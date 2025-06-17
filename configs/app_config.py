import os


class AppConfig:
    @staticmethod
    def get_valid_api_keys():
        if not os.getenv("X_API_KEY"):
            raise ValueError("X_API_KEY is not set")

        return {os.getenv("X_API_KEY")}

    @staticmethod
    def get_allowed_origins():
        if not os.getenv("ALLOWED_ORIGINS"):
            raise ValueError("ALLOWED_ORIGINS is not set")

        return os.getenv("ALLOWED_ORIGINS").split(",")

    @staticmethod
    def get_redis_connection_string():
        if not os.getenv("REDIS_CONNECTION_STRING"):
            raise ValueError("REDIS_CONNECTION_STRING is not set")

        return os.getenv("REDIS_CONNECTION_STRING")

    @staticmethod
    def get_queue_exchange_name():
        if not os.getenv("QUEUE_EXCHANGE_NAME"):
            raise ValueError("QUEUE_EXCHANGE_NAME is not set")

        return os.getenv("QUEUE_EXCHANGE_NAME")

    @staticmethod
    def get_request_limit():
        if not os.getenv("REQUEST_LIMIT"):
            return 30

        return int(os.getenv("REQUEST_LIMIT"))

    @staticmethod
    def get_request_time_window():
        if not os.getenv("REQUEST_TIME_WINDOW"):
            return 60

        return int(os.getenv("REQUEST_TIME_WINDOW"))
