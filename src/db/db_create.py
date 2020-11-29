from db.models import UserEmbeddingStorage, ScienceJobEmbeddingStorage, ProjectEmbeddingStorage
from db.service import session_scope
import torch


# def get_or_create(session, Model, defaults=None, **kwargs):
#     instance = session.query(Model).filter_by(**kwargs).first()
#     if instance:
#         return instance
#     else:
#         kwargs |= defaults or {}
#         instance = Model(**kwargs)
#         session.add(instance)
#         return instance


def update_or_create_user_descriptor(user_id: int, descriptor: torch.Tensor):
    with session_scope() as s:
        user = create_user_storage_if_not_exists(
            session=s,
            user_id=user_id,
            descriptor=descriptor
        )
        user.embedding = descriptor.tolist()
        s.flush()
        return user


def create_user_storage_if_not_exists(session, user_id: int, descriptor: torch.Tensor):
    instance = session.query(UserEmbeddingStorage).filter_by(user_id=user_id).first()
    if instance:
        return instance
    else:
        instance = UserEmbeddingStorage(
            user_id=user_id,
            embedding=descriptor.tolist(),
        )
        session.add(instance)
        session.commit()
        return instance


def save_science_job_object_into_db(
        descriptor: torch.Tensor,
        user_id: int
):
    with session_scope() as s:
        instance = ScienceJobEmbeddingStorage(
            user_id=user_id,
            embedding=descriptor.tolist(),
        )
        s.add(instance)
        s.commit()


def save_project_object_into_db(
        descriptor: torch.Tensor,
        project_id: int
):
    with session_scope() as s:
        instance = ProjectEmbeddingStorage(
            project_id=project_id,
            embedding=descriptor.tolist(),
        )
        s.add(instance)
        s.commit()
