import json
import logging
from datetime import datetime

# When running in a container, JSON logging is much easier to parse than plain text


class JSONFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)


def setup_logging():
    """Configure JSON logging for the application."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    
    logger = logging.getLogger("uvicorn.access")
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    
    logger = logging.getLogger("tasks_api")
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
