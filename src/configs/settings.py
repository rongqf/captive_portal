import os

from logging.config import dictConfig


LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(LOCAL_PATH, ".."))
PROJECT_NAME = 'captive portal'
PORT = 8000
DEBUG = True


DB_URI_OTC = 'postgresql+psycopg2://captive_portal:captive_portal@192.168.1.81:5432/captive_portal'


from .site_settings import *

RELOAD = DEBUG
DB_ECHO = DEBUG
LOG_DATA_FRAME_ALL = DEBUG
if LOG_DATA_FRAME_ALL:
    from utils.ghlogger import GHLogger
    
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "formatter": {
                "format": "{asctime} | {levelname} | [{process}: {processName}] {name}: {filename}:{lineno}: {funcName}: {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "formatter",
            },
        },
        "loggers": {
            "common": {
                "handlers": ["console"],
                "level": LOG_LEVEL,
                "propagage": False,
            },
        },
    }
)
