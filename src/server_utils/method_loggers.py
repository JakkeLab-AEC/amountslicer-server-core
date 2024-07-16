import logging
from functools import wraps
from src.config import ENVIRONMENT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Logger:
    @staticmethod
    def log_method(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if ENVIRONMENT == "dev":
                args_info = [(type(arg).__name__, arg) for arg in args]
                kwargs_info = {k: type(v).__name__ for k, v in kwargs.items()}
                logger.info(f"Executing {func.__name__} with arguments types {args_info} and kwargs types {kwargs_info}")
            result = func(*args, **kwargs)
            if ENVIRONMENT == "dev":
                logger.info(f"{func.__name__} returned type {type(result).__name__}")
            return result
        return wrapper

    @staticmethod
    def log_error(message: str):
        logger.error(message)

    @staticmethod
    def log_info(message: str):
        logger.info(message)

    @staticmethod
    def log_debug(message: str):
        logger.debug(message)