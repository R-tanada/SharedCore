import logging
import logging.handlers

from pythonjsonlogger import jsonlogger

DEBUG = logging.DEBUG
ERROR = logging.ERROR
INFO = logging.INFO
WARN = logging.WARN
WARNING = logging.WARNING

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

stream_formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d [%(levelname)-8s] %(module)s:%(lineno)d >> %(message)s",
    datefmt="%H:%M:%S",
)


class StreamFilter(logging.Filter):
    def filter(self, record):
        return "message" not in record.getMessage()


streamHandler = logging.StreamHandler()
streamHandler.setFormatter(stream_formatter)
logger.addHandler(streamHandler)
streamHandler.addFilter(StreamFilter())

json_formatter = jsonlogger.JsonFormatter(
    fmt="%(asctime)s %(module)s %(lineno)d  %(message)s",
    json_ensure_ascii=False,
)


def set_file_handler(filename, fileLogLevel, mode, filt=None):
    __fileHandler = logging.FileHandler(filename=filename, mode=mode)
    __fileHandler.setFormatter(json_formatter)
    __fileHandler.setLevel(fileLogLevel)
    logger.addHandler(__fileHandler)
    if filt:
        __fileHandler.addFilter(LogTextFilter(filtText=filt))


class LogTextFilter(logging.Filter):
    def __init__(self, filtText):
        self.filt_text = filtText

    def filter(self, record):
        if self.filt_text in record.getMessage():
            return True
        return False
