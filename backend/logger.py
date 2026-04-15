"""
Centralized logging configuration for the Srvey backend.

Provides structured logging for:
- HTTP requests and responses
- Database operations
- Authentication events
- Error handling
- Service layer operations
"""

import logging
import logging.handlers
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
import json

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Log file paths
ERROR_LOG = LOG_DIR / "errors.log"
ACCESS_LOG = LOG_DIR / "access.log"
DEBUG_LOG = LOG_DIR / "debug.log"


class JSONFormatter(logging.Formatter):
    """Format log records as JSON for better parsing and analysis."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add custom fields if present
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "endpoint"):
            log_data["endpoint"] = record.endpoint
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "response_time"):
            log_data["response_time_ms"] = record.response_time
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        return json.dumps(log_data)


def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None,
    json_format: bool = True,
) -> logging.Logger:
    """
    Configure a logger with both file and console handlers.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file
        json_format: Whether to use JSON formatting

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10_000_000,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create logger instances
app_logger = setup_logger("app", logging.INFO)
error_logger = setup_logger("error", logging.ERROR, ERROR_LOG)
access_logger = setup_logger("access", logging.INFO, ACCESS_LOG, json_format=True)
debug_logger = setup_logger("debug", logging.DEBUG, DEBUG_LOG, json_format=False)


def log_request(
    method: str,
    endpoint: str,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
):
    """Log incoming HTTP request."""
    record = logging.LogRecord(
        name="access",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=f"{method} {endpoint}",
        args=(),
        exc_info=None,
    )
    if user_id:
        record.user_id = user_id
    if endpoint:
        record.endpoint = endpoint
    if method:
        record.method = method
    if request_id:
        record.request_id = request_id

    access_logger.handle(record)


def log_response(
    method: str,
    endpoint: str,
    status_code: int,
    response_time_ms: float,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
):
    """Log HTTP response."""
    record = logging.LogRecord(
        name="access",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=f"{method} {endpoint} -> {status_code} ({response_time_ms:.2f}ms)",
        args=(),
        exc_info=None,
    )
    if user_id:
        record.user_id = user_id
    if endpoint:
        record.endpoint = endpoint
    if method:
        record.method = method
    if status_code:
        record.status_code = status_code
    if response_time_ms:
        record.response_time = response_time_ms
    if request_id:
        record.request_id = request_id

    access_logger.handle(record)


def log_error(
    error: Exception,
    endpoint: Optional[str] = None,
    user_id: Optional[str] = None,
    context: Optional[dict] = None,
):
    """Log error with full context."""
    record = logging.LogRecord(
        name="error",
        level=logging.ERROR,
        pathname="",
        lineno=0,
        msg=f"Error in {endpoint or 'unknown endpoint'}: {str(error)}",
        args=(),
        exc_info=(type(error), error, error.__traceback__),
    )
    if endpoint:
        record.endpoint = endpoint
    if user_id:
        record.user_id = user_id
    if context:
        record.context = context

    error_logger.handle(record)


def log_auth_event(event: str, user_id: Optional[str] = None, success: bool = True):
    """Log authentication events."""
    status = "success" if success else "failed"
    message = f"Auth {event}: {status}"
    if user_id:
        message += f" (user: {user_id})"

    record = logging.LogRecord(
        name="app",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=message,
        args=(),
        exc_info=None,
    )
    if user_id:
        record.user_id = user_id

    app_logger.handle(record)


def log_database_operation(
    operation: str,
    collection: str,
    user_id: Optional[str] = None,
    success: bool = True,
    duration_ms: Optional[float] = None,
):
    """Log database operations."""
    status = "success" if success else "failed"
    message = f"DB {operation} on {collection}: {status}"
    if duration_ms:
        message += f" ({duration_ms:.2f}ms)"

    record = logging.LogRecord(
        name="app",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg=message,
        args=(),
        exc_info=None,
    )
    if user_id:
        record.user_id = user_id

    app_logger.handle(record)


def log_service_operation(
    service_name: str,
    operation: str,
    success: bool = True,
    duration_ms: Optional[float] = None,
    error: Optional[str] = None,
):
    """Log service layer operations."""
    level = logging.ERROR if not success else logging.INFO
    status = "success" if success else "failed"
    message = f"{service_name}.{operation}: {status}"

    if duration_ms:
        message += f" ({duration_ms:.2f}ms)"
    if error:
        message += f" - {error}"

    record = logging.LogRecord(
        name="app",
        level=level,
        pathname="",
        lineno=0,
        msg=message,
        args=(),
        exc_info=None,
    )

    app_logger.handle(record)
