import logging
import sys

from src.platform.config import settings


class AppLogger:
    def __init__(self, name: str) -> None:
        self._logger = logging.getLogger(name)
        self._logger.setLevel(settings.log_level.upper())

        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(settings.log_level.upper())
            formatter = logging.Formatter(settings.log_format)
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)

    def info(self, msg: str, *args: object) -> None:
        self._logger.info(msg, *args)

    def error(self, msg: str, *args: object) -> None:
        self._logger.error(msg, *args)

    def warning(self, msg: str, *args: object) -> None:
        self._logger.warning(msg, *args)

    def debug(self, msg: str, *args: object) -> None:
        self._logger.debug(msg, *args)
