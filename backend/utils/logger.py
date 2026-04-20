import logging
import sys
from datetime import datetime
from typing import Optional

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the given name.

    Args:
        name: Usually __name__ of the calling module

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


# Create module-level logger
logger = get_logger("app")


def log_request(method: str, endpoint: str, params: Optional[dict] = None) -> None:
    """Log incoming API request.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path
        params: Optional request parameters
    """
    message = f"Request: {method} {endpoint}"
    if params:
        message += f" | Params: {params}"
    logger.info(message)


def log_response(method: str, endpoint: str, status_code: int, duration_ms: Optional[float] = None) -> None:
    """Log API response.

    Args:
        method: HTTP method
        endpoint: API endpoint path
        status_code: HTTP status code
        duration_ms: Optional response time in milliseconds
    """
    message = f"Response: {method} {endpoint} | Status: {status_code}"
    if duration_ms:
        message += f" | Duration: {duration_ms:.2f}ms"

    if status_code >= 400:
        logger.warning(message)
    else:
        logger.info(message)


def log_error(error: Exception, context: Optional[str] = None) -> None:
    """Log error with optional context.

    Args:
        error: Exception instance
        context: Optional context string
    """
    message = f"Error: {str(error)}"
    if context:
        message = f"{context} - {message}"
    logger.error(message, exc_info=True)


def log_db_operation(operation: str, table: str, record_id: Optional[str] = None) -> None:
    """Log database operation.

    Args:
        operation: Operation type (CREATE, READ, UPDATE, DELETE)
        table: Table name
        record_id: Optional record ID
    """
    message = f"DB: {operation} on {table}"
    if record_id:
        message += f" | ID: {record_id}"
    logger.debug(message)