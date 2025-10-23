from sqlalchemy.orm import Session
from sqlalchemy import select
from .orm import fastapi
from typing import List

def get_fastapi(session: Session) -> List[fastapi]:
    return list(session.scalars(select(fastapi)))
