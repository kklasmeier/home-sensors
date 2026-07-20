import argparse
import datetime
import logging
import time

import mysql.connector
import requests

from db import connect

MAX_RETRIES = 5
API_TIMEOUT = 5

parser = argparse.ArgumentParser(
    description="Read sensor data from a web service and insert into a database"
)
parser.add_argument("ip_address", type=str, help="IP address of the web service")
parser.add_argument("location", type=str, help="Location to be inserted into the database")
args = parser.parse_args()

log_format = f"%(asctime)s ({args.location}): %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format, datefmt="%Y-%m-%d %H:%M:%S")

REQUIRED_FIELDS = ("Temperature_F", "Heat Index_F", "Humidity_%", "Pressure_inHg")


def reading_is_valid(data):
    if not isinstance(data, dict):
        return False
    if data.get("error"):
        return False
    return all(data.get(field) is not None for field in REQUIRED_FIELDS)


while True:
    for i in range(MAX_RETRIES):
        connection = None
        cursor = None
        try:
            logging.info("Taking a reading")

            session = requests.Session()
            response = session.get(f"http://{args.ip_address}/data.json", timeout=API_TIMEOUT)
            data = response.json()

            if data is None:
                raise ValueError("No data returned from API")

            if not reading_is_valid(data):
                err = (
                    data.get("error", "missing required fields")
                    if isinstance(data, dict)
                    else "invalid response"
                )
                logging.warning(f"Skipping insert — sensor returned: {err}")
                break

            connection = connect()

            if connection.is_connected():
                cursor = connection.cursor()

                insert_query = """
                INSERT INTO sensor_readings (reading_dttm, location, temperature_f, heat_index_f, humidity_pct, pressure_inHg, created_by)
                VALUES (NOW(), %s, %s, %s, %s, %s, %s)
                """
                values = (
                    args.location,
                    data.get("Temperature_F"),
                    data.get("Heat Index_F"),
                    data.get("Humidity_%"),
                    data.get("Pressure_inHg"),
                    "API User",
                )
                cursor.execute(insert_query, values)

                summary_date = datetime.date.today().isoformat()
                cursor.execute(
                    """
                  INSERT INTO sensor_readings_summary (summary_date, location, max_temperature_f, min_temperature_f, max_heat_index_f, min_heat_index_f, max_humidity_pct, min_humidity_pct, max_pressure_inHg, min_pressure_inHg)
                  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  ON DUPLICATE KEY UPDATE
                    max_temperature_f = GREATEST(max_temperature_f, VALUES(max_temperature_f)),
                    min_temperature_f = LEAST(min_temperature_f, VALUES(min_temperature_f)),
                    max_heat_index_f = GREATEST(max_heat_index_f, VALUES(max_heat_index_f)),
                    min_heat_index_f = LEAST(min_heat_index_f, VALUES(min_heat_index_f)),
                    max_humidity_pct = GREATEST(max_humidity_pct, VALUES(max_humidity_pct)),
                    min_humidity_pct = LEAST(min_humidity_pct, VALUES(min_humidity_pct)),
                    max_pressure_inHg = GREATEST(max_pressure_inHg, VALUES(max_pressure_inHg)),
                    min_pressure_inHg = LEAST(min_pressure_inHg, VALUES(min_pressure_inHg))
                  """,
                    (
                        summary_date,
                        args.location,
                        data.get("Temperature_F"),
                        data.get("Temperature_F"),
                        data.get("Heat Index_F"),
                        data.get("Heat Index_F"),
                        data.get("Humidity_%"),
                        data.get("Humidity_%"),
                        data.get("Pressure_inHg"),
                        data.get("Pressure_inHg"),
                    ),
                )
                connection.commit()

            break

        except (requests.exceptions.RequestException, ValueError) as e:
            logging.error(f"Request error: '{e}'")
            if i < MAX_RETRIES - 1:
                logging.info(f"Retrying in {2 ** (i + 1)} seconds...")
                time.sleep(2 ** (i + 1))
                continue
            logging.error("All retry attempts failed. Check the server or network connection.")

        except mysql.connector.Error as e:
            logging.error(f"Database Error: '{e}'")
            break

        except Exception as e:
            logging.error(f"Unhandled error: '{e}'")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    time.sleep(60)
