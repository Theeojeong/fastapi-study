from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from fastapi import Depends
from .orm import Todo
from .connection import get_db
from typing import List

class ToDoRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_todos(self) -> List[Todo]:
        return list(self.session.scalars(select(Todo)))
        # Raw SQL: cur.execute("SELECT * FROM todos")
        #          rows = cur.fetchall()

    def get_todo_by_todo_id(self, todo_id: int) -> Todo | None:
        return self.session.scalar(select(Todo).where(Todo.id == todo_id))
        # Raw SQL: cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        #          row = cur.fetchone()

    def create_todo(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)  # -> 여기서 id가 생성이 된다
        return todo
        # Raw SQL: cur.execute(
        #              "INSERT INTO todos (contents, is_done, user_id) VALUES (%s, %s, %s)",
        #              (todo.contents, todo.is_done, todo.user_id)
        #          )
        #          conn.commit()
        #          todo_id = cur.lastrowid  # 생성된 id 가져오기

    def update_todo(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo
        # Raw SQL: cur.execute(
        #              "UPDATE todos SET contents = %s, is_done = %s WHERE id = %s",
        #              (todo.contents, todo.is_done, todo.id)
        #          )
        #          conn.commit()

    def delete_todo(self, todo_id: int) -> None:
        self.session.execute(delete(Todo).where(Todo.id == todo_id))
        self.session.commit()
        # Raw SQL: cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        #          conn.commit()


# =============================================================================
# 📌 SQLAlchemy vs Raw SQL 문법 비교 요약
# =============================================================================
#
# | 작업     | SQLAlchemy                              | Raw SQL (pymysql)                           |
# |----------|----------------------------------------|---------------------------------------------|
# | 전체조회 | session.scalars(select(Todo))          | cur.execute("SELECT * FROM todos")          |
# | 단일조회 | select(Todo).where(Todo.id == id)      | "SELECT * FROM todos WHERE id = %s"         |
# | 생성     | session.add(todo) + commit()           | cur.execute("INSERT INTO ...") + commit()   |
# | 수정     | session.add(todo) + commit()           | cur.execute("UPDATE ... SET ...") + commit()|
# | 삭제     | session.execute(delete(Todo).where())  | cur.execute("DELETE FROM ...") + commit()   |
#
# =============================================================================
