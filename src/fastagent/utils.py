"""Utility functions."""

import logging
from datetime import UTC, datetime


class LoggingFormatter(logging.Formatter):
    """Custom formatter for logging."""

    def format(self, record: logging.LogRecord) -> str:
        """Format the record to a string.

        Args:
            record: The record to format.

        Returns:
            The formatted record as a string.
        """
        timestamp = datetime.now(UTC).astimezone().isoformat()

        log_msg = (
            f"time={timestamp}"
            f" level={record.levelname}"
            f" msg='{record.getMessage()}'"
        )

        if hasattr(record, "request") and (req := record.request):
            log_msg += (
                f" ip={req.client.host}:{req.client.port}"
                f" proto={req.scope['scheme'].upper()}/{req.scope['http_version']}"
                f" method={req.method}"
                f" uri={req.url.path}"
            )

        return log_msg
