import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# TODO change on MARIADB
logger = logging.getLogger(__name__)
user = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
db = os.environ.get("POSTGRES_DB")

# recognizer-db
SQLALCHEMY_DATABASE_URL = 'postgres://postgres:1234567@recognizer_db:5432/recognizer_db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def session_scope() -> SessionLocal:
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal(bind=engine)
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
