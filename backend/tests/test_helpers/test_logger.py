import json
import logging
import os
import importlib
from unittest.mock import patch


def test_logger_name():
    from src.helpers.logger import logger
    assert logger.name == "expense_tracker"


def test_logger_dev_level():
    with patch.dict("os.environ", {"ENV": "development"}, clear=False):
        import src.config
        importlib.reload(src.config)
        import src.helpers.logger as logger_mod
        importlib.reload(logger_mod)
        assert logger_mod.logger.level == logging.DEBUG


def test_logger_dev_has_console_handler():
    with patch.dict("os.environ", {"ENV": "development"}, clear=False):
        import src.config
        importlib.reload(src.config)
        import src.helpers.logger as logger_mod
        importlib.reload(logger_mod)
        handler_types = [type(h) for h in logger_mod.logger.handlers]
        assert logging.StreamHandler in handler_types


def test_logger_prod_level():
    with patch.dict("os.environ", {"ENV": "production"}, clear=False):
        import src.config
        importlib.reload(src.config)
        import src.helpers.logger as logger_mod
        importlib.reload(logger_mod)
        assert logger_mod.logger.level == logging.INFO


def test_logger_prod_has_file_handler():
    log_file = "test_app.log"
    with patch.dict("os.environ", {"ENV": "production", "LOG_FILE": log_file}, clear=False):
        import src.config
        importlib.reload(src.config)
        import src.helpers.logger as logger_mod
        importlib.reload(logger_mod)
        handler_types = [type(h) for h in logger_mod.logger.handlers]
        assert logging.FileHandler in handler_types
        for h in list(logger_mod.logger.handlers):
            if isinstance(h, logging.FileHandler):
                h.close()
                logger_mod.logger.removeHandler(h)
    for f in [log_file, log_file.replace(".log", ".json.log")]:
        if os.path.exists(f):
            os.remove(f)


def test_logger_prod_has_json_handler():
    log_file = "test_json.log"
    with patch.dict("os.environ", {"ENV": "production", "LOG_FILE": log_file}, clear=False):
        import src.config
        importlib.reload(src.config)
        import src.helpers.logger as logger_mod
        importlib.reload(logger_mod)
        json_handlers = [h for h in logger_mod.logger.handlers
                         if isinstance(h, logging.FileHandler) and isinstance(h.formatter, logger_mod.JsonFormatter)]
        assert len(json_handlers) >= 1
        for h in list(logger_mod.logger.handlers):
            if isinstance(h, logging.FileHandler):
                h.close()
                logger_mod.logger.removeHandler(h)
    for f in [log_file, log_file.replace(".log", ".json.log")]:
        if os.path.exists(f):
            os.remove(f)


def test_logger_has_at_least_one_handler():
    from src.helpers.logger import logger
    assert len(logger.handlers) >= 1


def test_json_formatter_output():
    from src.helpers.logger import JsonFormatter
    fmt = JsonFormatter()
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="test.py",
        lineno=1, msg="hello %s", args=("world",), exc_info=None,
    )
    output = fmt.format(record)
    parsed = json.loads(output)
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "hello world"
    assert "timestamp" in parsed
    assert "module" in parsed


def test_json_formatter_includes_exception():
    from src.helpers.logger import JsonFormatter
    fmt = JsonFormatter()
    try:
        raise ValueError("boom")
    except ValueError:
        import sys
        exc_info = sys.exc_info()
    record = logging.LogRecord(
        name="test", level=logging.ERROR, pathname="test.py",
        lineno=1, msg="fail", args=(), exc_info=exc_info,
    )
    output = fmt.format(record)
    parsed = json.loads(output)
    assert "exception" in parsed
    assert "boom" in parsed["exception"]


def test_setup_logger_custom_name():
    from src.helpers.logger import setup_logger
    custom = setup_logger(name="custom_test", env="development")
    assert custom.name == "custom_test"
    assert custom.level == logging.DEBUG


def test_setup_logger_prod_creates_files():
    log_file = "test_setup.log"
    from src.helpers.logger import setup_logger
    prod_logger = setup_logger(name="prod_test", env="production", log_file=log_file)
    prod_logger.info("test message")
    for h in list(prod_logger.handlers):
        if isinstance(h, logging.FileHandler):
            h.close()
            prod_logger.removeHandler(h)
    assert os.path.exists(log_file)
    json_file = log_file.replace(".log", ".json.log")
    assert os.path.exists(json_file)
    with open(json_file) as f:
        line = f.readline()
        parsed = json.loads(line)
        assert parsed["message"] == "test message"
    for f_path in [log_file, json_file]:
        os.remove(f_path)
