
import logging
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from utils.singleton import Singleton, SingletonMate


from utils.rds import (
    get_reload_info,
    set_reload_info,
)
from configs import settings

logger = logging.getLogger("common")

engine = create_engine(
    settings.DB_URI_OTC,
    echo=settings.DB_ECHO,
    pool_timeout=5,
    pool_pre_ping=True,
    pool_recycle=3600,
)
DBSession = sessionmaker(engine)

@contextmanager
def get_db_session():
    session = DBSession()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    pass