import json
import logging
import datetime as dt


class JSONFormatter(logging.Formatter):
    def __init__(self, fields: list, datefmt: str = DEFAULT_DATE_FORMAT):
        self.datefmt = datefmt

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record as a JSON string.
        """
        return json.dumps(record.__dict__)

    def formatException(self, exc_info: logging.Log) -> str:
        """
        Format the log record as a JSON string.
        """
        print(type(exc_info))
        return json.dumps(record.__dict__)
