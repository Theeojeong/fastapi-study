from fastapi import FastAPI, Body, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import get_db
from database.repository import (
    get_todos,
    get_todo_by_todo_id,
    create_todo,
    update_todo,
    delete_todo,
)
from database.orm import Todo
from schema.response import ListTodosResponse, TodoSchema
from schema.request import TodoRequestBody
from typing import List

app = FastAPI()

# ===================GET======================


@app.get("/")
def health_check_handler():
    return {"Hi": "HelloWorld"}


@app.get("/todos")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
):
    rets: List[Todo] = get_todos(session=session)

    if order == "DESC":
        return ListTodosResponse(
            todos=[TodoSchema.model_validate(ret) for ret in rets[::-1]]
        )
    return ListTodosResponse(todos=[TodoSchema.model_validate(ret) for ret in rets])


@app.get("/todo/{todo_id}", status_code=200, name="todo 단일 조회")
def get_todo_handler(
    todo_id: int,
    session: Session = Depends(get_db),
):
    ret: Todo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)

    if ret:
        return TodoSchema.model_validate(ret)
    raise HTTPException(status_code=400, detail="Todo Not Found")


# ===================POST======================


@app.post("/todos")
def post_todo_handler(
    request: TodoRequestBody,
    session: Session = Depends(get_db),
):
    ret: Todo = Todo.create(request=request)
    ret: Todo = create_todo(session=session, todo=ret)
    return TodoSchema.model_validate(ret)


# ===================PATCH======================


@app.patch("/todo/{todo_id}", status_code=200)
def patch_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    ret: Todo | None = get_todo_by_todo_id(
        session=session,
        todo_id=todo_id,
    )
    if ret:
        ret.done() if is_done else ret.undone()
        ret = update_todo(session=session, todo=ret)
        return TodoSchema.model_validate(ret)

    raise HTTPException(status_code=404, detail="Todo Not Found")


# ===================DELEET======================


@app.delete("/todo/{todo_id}", status_code=204)
def delete_todo_handler(todo_id: int, session: Session = Depends(get_db),):

    ret: Todo | None = get_todo_by_todo_id(
        session=session,
        todo_id=todo_id,
    )
    if not ret:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    delete_todo(session=session, todo_id=todo_id)
