from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import Date
from db.service import Base
import datetime
import pandas as pd


class ProjectEmbeddingStorage(Base):
    __tablename__ = "project_embedding_storage"

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, index=True
    )

    project_id = Column(Integer, nullable=False, index=True)
    embedding = Column(ARRAY(Float))


class UserEmbeddingStorage(Base):
    __tablename__ = "user_embedding_storage"

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, index=True
    )

    user_id = Column(Integer, nullable=False, index=True)
    embedding = Column(ARRAY(Float))


class ScienceJobEmbeddingStorage(Base):
    __tablename__ = "science_job_embedding_storage"

    id = Column(Integer, primary_key=True, autoincrement=True)

    created_at = Column(
        DateTime(timezone=True), default=datetime.datetime.utcnow, index=True
    )
    user_id = Column(Integer, nullable=False, index=True)
    embedding = Column(ARRAY(Float))


metadata = Base.metadata
