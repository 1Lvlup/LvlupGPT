import logging
import typing as t
from colorama import Style
from google.cloud.logging_v2.handlers import CloudLoggingFilter, StructuredLogHandler
from google.cloud.logging_v2.types import StructuredLog
from datetime import datetime

remove_color_codes = lambda msg: re.sub(r'\x1b\[[0-9;]*[mK]', '', msg)

class AutoGptFormatter(logging.Formatter):
    LEVEL_COLOR_MAP = {
        10: '',  # DEBUG
        20: '',  # INFO
        30: '\x1b[31m',  # WARNING
        40: '\x1b[31m',  # ERROR
        50: '\x1b[31m',  # CRITICAL
    }

    def __init__(self, no_color: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.no_color = no_color

    def formatTime(self, record: logging.LogRecord, datefmt: str = None) -> str:
        if datefmt is None:
            datefmt = '%Y-%m-%d %H:%M:%S'
        return datetime.fromtimestamp(record.created).strftime(datefmt)

    def formatException(self, exc_info: t.Optional[t.Tuple[t.Type[BaseException], BaseException, t.Traceback]] = None) -> str:
        result = super().formatException(exc_info)
        if not self.no_color:
            result = '\x1b[31m' + result + '\x1b[0m'
        return result

    def formatMessage(self, message: t.Any) -> str:
        if not self.no_color:
            message = remove_color_codes(message)
        return message

    def format(self, record: logging.LogRecord) -> str:
        message = self.formatMessage(record.msg)
        record.msg = message
        return super().format(record)

    def format_record(self, record: logging.LogRecord) -> str:
        message = self.formatMessage(record.msg)
        record.msg = message
        if not self.no_color:
            record.msg = remove_color_codes(record.msg)
        return super().format(record)

    def format_message(self, record: logging.LogRecord) -> str:
        message = super().formatMessage(record)
        if not self.no_color:
            message = remove_color_codes(message)
        return message

class StructuredLog
