from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    @staticmethod
    def get_variable(key, default=None):
        return os.getenv(key, default)
    @staticmethod
    def get_variable_int(key, default=None):
        value = os.getenv(key, default)
        return int(value) if value is not None else default
    @staticmethod
    def get_variable_list(key, default=None):
        value = os.getenv(key)
        if not value:
            return default
        return [int(x.strip()) for x in value.split(",") if x.strip()]