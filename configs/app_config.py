import os


class AppConfig:
    VALID_API_KEYS = {os.getenv("X_API_KEY")}
