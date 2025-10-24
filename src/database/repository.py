from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from .orm import Todo
from typing import List

def get_todos(session: Session) -> List[Todo]:
    return list(session.scalars(select(Todo)))


def get_todo_by_todo_id(session: Session, todo_id: int) -> Todo | None:
    return session.scalar(select(Todo).where(Todo.id == todo_id))

def create_todo(session: Session, todo: Todo) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(todo)  # -> 여기서 id가 생성이 된다
    return todo


def update_todo(session: Session, todo: Todo) -> Todo:
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

def delete_todo(session: Session, todo_id: int) -> None:
    session.execute(delete(Todo).where(Todo.id == todo_id))
    session.commit()
