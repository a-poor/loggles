import sys
import enum
import time
import json
import logging
import datetime as dt
from typing import Optional, Dict, Any, Union

class LogRecordData(enum.Enum):
    """
    Enum for the log record data.
    """
    ASCTIME = 0
    CREATED = 1
    FILENAME = 2
    FUNC_NAME = 3
    LEVELNAME = 4
    LEVELNO = 5
    LINENO = 6
    MESSAGE = 7
    MODULE = 8
    MSECS = 9
    NAME = 10
    PATHNAME = 11
    PROCESS = 12
    PROCESS_NAME = 13
    RELATIVE_CREATED = 14
    THREAD = 15
    THREAD_NAME = 16

    @classmethod
    def _get_fmt_string(cls, d: 'LogRecordData') -> str:
        if d == cls.ASCTIME:
            return '"%(asctime)s"'
        elif d == cls.CREATED:
            return "%(created)f"
        elif d == cls.FILENAME:
            return '"%(filename)s"'
        elif d == cls.FUNC_NAME:
            return '"%(funcName)s"'
        elif d == cls.LEVELNAME:
            return '"%(levelname)s"'
        elif d == cls.LEVELNO:
            return '"%(levelno)s"'
        elif d == cls.LINENO:
            return "%(lineno)d"
        elif d == cls.MESSAGE:
            return '%(message)s'
        elif d == cls.MODULE:
            return '"%(module)s"'
        elif d == cls.MSECS:
            return "%(msecs)d"
        elif d == cls.NAME:
            return '"%(name)s"'
        elif d == cls.PATHNAME:
            return '"%(pathname)s"'
        elif d == cls.PROCESS:
            return "%(process)d"
        elif d == cls.PROCESS_NAME:
            return '"%(processName)s"'
        elif d == cls.RELATIVE_CREATED:
            return "%(relativeCreated)d"
        elif d == cls.THREAD:
            return "%(thread)d"
        elif d == cls.THREAD_NAME:
            return '"%(threadName)s"'
        else:
            return str(d)

def create_json_log_formatter(fields: Dict[str, Any]) -> str:
    if not isinstance(fields, dict):
        raise TypeError("`fields` needs to be of type `dict`")
    def fmt(f) -> str:
        if isinstance(f, LogRecordData):
            return LogRecordData._get_fmt_string(f)
        return json.dumps(f)
    return "{" + ", ".join([
        f'{json.dumps(k)}: {fmt(v)}' for k, v in fields.items()
    ]) + LogRecordData._get_fmt_string(LogRecordData.MESSAGE) + "}"


class JSONLogAdapter(logging.LoggerAdapter):
    def __init__(self, logger: logging.Logger, fields: Optional[Dict[str, Any]] = None, extra: Optional[Dict[str, Any]] = None):
        self._fields = fields or {}
        super().__init__(logger, extra or {})

    def get_formatter(self) -> str:
        pass

    def _format_message(self, data: Dict[str, Any] = {}):
        return ", ".join([f"{json.dumps(k)}: {json.dumps(v)}" for k, v in data.items()])
    
    def log(self, level: int, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        if isinstance(msg, str):
            msg = {"message": msg}
        if isinstance(msg, dict):
            prefix = ", " if (len(self._fields) and len(msg)) else ""
            m = prefix + self._format_message(msg)
        else:
            m = ""
        return self.logger._log(level, m, args, **kwargs)

    def debug(self, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        self.log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        self.log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        self.log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        self.log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg: Union[None, str, Dict[str, Any]] = None, *args, **kwargs):
        self.log(logging.CRITICAL, msg, *args, **kwargs)


fields = {
    "timestamp": LogRecordData.ASCTIME,
    "name": LogRecordData.NAME,
    "level": LogRecordData.LEVELNAME,
    "relativeCreated": LogRecordData.RELATIVE_CREATED,
}

base = logging.getLogger(__name__)
log = JSONLogAdapter(base, fields)
fmt = logging.Formatter(create_json_log_formatter(fields))
sh = logging.StreamHandler(sys.stdout)
sh.setFormatter(fmt)
base.addHandler(sh)
base.setLevel(logging.INFO)

log.info("Starting...")
time.sleep(0.1)
log.info()
time.sleep(0.3)
log.error({"error": "Something went wrong!"})
time.sleep(0.2)
log.info("Done.")

