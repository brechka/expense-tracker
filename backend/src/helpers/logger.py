import json
import logging
import sys
from datetime import datetime, timezone
from src.config import ENV, LOG_FILE


class JsonFormatter(logging.Formatter):
    """Structured JSON formatter for external log management systems."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry)


def setup_logger(
    name: str = "expense_tracker",
    env: str | None = None,
    log_file: str | None = None,
) -> logging.Logger:
    _env = env or ENV
    _log_file = log_file or LOG_FILE

    _logger = logging.getLogger(name)
    _logger.handlers.clear()
    _logger.setLevel(logging.DEBUG if _env == "development" else logging.INFO)

    text_fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    json_fmt = JsonFormatter()

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(text_fmt)

    if _env == "development":
        console.setLevel(logging.DEBUG)
        _logger.addHandler(console)
    else:
        # Production: file (text) + JSON file (structured) + console (warnings+)
        file_handler = logging.FileHandler(_log_file)
        file_handler.setFormatter(text_fmt)
        file_handler.setLevel(logging.INFO)
        _logger.addHandler(file_handler)

        json_file = _log_file.replace(".log", ".json.log")
        json_handler = logging.FileHandler(json_file)
        json_handler.setFormatter(json_fmt)
        json_handler.setLevel(logging.INFO)
        _logger.addHandler(json_handler)

        console.setLevel(logging.WARNING)
        _logger.addHandler(console)

    return _logger


logger = setup_logger()
