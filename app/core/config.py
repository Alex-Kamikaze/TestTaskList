from pydantic_settings import BaseSettings
from logging import DEBUG, INFO
from typing import Literal


class DevSettings(BaseSettings):
    DATABASE_URI: str = "sqlite:///db.sqlite3"  # Для разработки и тестирования приложения
    LOGGING_LEVEL: Literal[10] = DEBUG
    HOST: str = "127.0.0.1"
    PORT: int = 8000


class ProductionSettings(BaseSettings):
    DATABASE_URI: str = "mysql+pymysql://root:shedF34A@localhost:3306/taskdb"
    LOGGING_LEVEL: Literal[20] = INFO
    HOST: str = "0.0.0.0"
    PORT: int = 8000


dev_settings = DevSettings()
prod_settings = ProductionSettings()
