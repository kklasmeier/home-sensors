from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str = "localhost"
    db_user: str = "hu"
    db_password: str = ""
    db_name: str = "homedata"

    api_host: str = "0.0.0.0"
    api_port: int = 8090

    collector_log_path: str = "/home/pi/HomeData/Logs/collect_data.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
