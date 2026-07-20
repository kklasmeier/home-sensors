import argparse
import logging
import time

import mysql.connector
import requests

from db import connect

MAX_RETRIES = 5
API_TIMEOUT = 5

parser = argparse.ArgumentParser(
    description="Read sump pump sensor data from a web service and insert into a database"
)
parser.add_argument("ip_address", type=str, help="IP address of the web service")
args = parser.parse_args()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s (SumpPump): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

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

            water_level = data.get("WaterLevel")
            water_level = 23 - 6 - water_level

            connection = connect()

            if connection.is_connected():
                cursor = connection.cursor()
                insert_query = """
                INSERT INTO sensor_readings_sump_pump (reading_dttm, water_level)
                VALUES (NOW(), %s)
                """
                cursor.execute(insert_query, (water_level,))
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

        except Exception as e:
            logging.error(f"Unhandled error: '{e}'")
            raise

        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    time.sleep(30)
