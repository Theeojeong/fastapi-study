from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from .orm import fastapi
from typing import List

def get_fastapi(session: Session) -> List[fastapi]:
    return list(session.scalars(select(fastapi)))


def get_fastapi_by_fastapi_id(session: Session, fastapi_id: int) -> fastapi | None:
    return session.scalar(select(fastapi).where(fastapi.id == fastapi_id))

def fastapi_create(session: Session, fastapi: fastapi) -> fastapi:
    session.add(fastapi)
    session.commit()
    session.refresh(fastapi) # -> 여기서 id가 생성이 된다
    return fastapi


def fastapi_update(session: Session, fastapi: fastapi) -> fastapi:
    session.add(fastapi)
    session.commit()
    session.refresh(fastapi)
    return fastapi

def fastapi_delete(session: Session, fastapi_id: int) -> None:
    session.execute(delete(fastapi).where(fastapi.id == fastapi_id))
    session.commit()