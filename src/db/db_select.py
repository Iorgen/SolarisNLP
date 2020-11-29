import pandas as pd

from db.models import UserEmbeddingStorage, ScienceJobEmbeddingStorage
from db.service import session_scope


def get_all_users_embeddings(photo_id: str):
    with session_scope() as s:
        person = pd.read_sql(s.query(UserEmbeddingStorage), s.bind)
    return person


def get_all_science_job_embeddings_by_user_id(user_id: int):
    with session_scope() as s:
        jobs = pd.read_sql(s.query(ScienceJobEmbeddingStorage).filter(
            ScienceJobEmbeddingStorage.user_id == user_id
        ).statement, s.bind)
    return jobs["embedding"]


def get_user_mapped_embeddings():
    with session_scope() as s:
        persons = pd.read_sql(s.query(UserEmbeddingStorage).statement, s.bind)
    return persons


def get_user_data_by_id(user_id: str):
    with session_scope() as s:
        pass
        # TODO
        #   select from db searchable and with user_id


def get_user_science_jobs_article(user_id: str):
    with session_scope() as s:
        # TODO
        #   select from db searchable and with user_id
        pass