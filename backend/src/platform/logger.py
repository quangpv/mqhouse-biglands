import logging
import os
import sys
from logging.handlers import RotatingFileHandler

from src.platform.config import settings


class AppLogger:
    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(settings.log_level.upper())

        if not self._logger.handlers:
            formatter = logging.Formatter(settings.log_format)

            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(settings.log_level.upper())
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

            log_dir = settings.log_dir
            if log_dir:
                file_handler = RotatingFileHandler(
                    os.path.join(log_dir, "app.log"),
                    maxBytes=10 * 1024 * 1024,
                    backupCount=5,
                )
                file_handler.setLevel(settings.log_level.upper())
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)

    def info(self, msg: str, *args: object) -> None:
        self._logger.info(msg, *args)

    def error(self, msg: str, *args: object) -> None:
        self._logger.error(msg, *args)

    def warning(self, msg: str, *args: object) -> None:
        self._logger.warning(msg, *args)

    def debug(self, msg: str, *args: object) -> None:
        self._logger.debug(msg, *args)
