# ------------9/9 학습 내용-------------
from databases.connection import get_db
from databases.repository import get_todos
from schemas.response import ListToDoResponse, ToDoSchema
from fastapi import FastAPI, HTTPException, Body, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from databases.orm import ToDo

app = FastAPI()

@app.get("/")
def health_check():
    return {"helloworld"}


@app.get("/todos", name="전체 조회 api")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db)):
    
    todos: List[ToDo] = get_todos(session=session)

    if order == "up":
        return ListToDoResponse(todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]])

    return ListToDoResponse(todos=[ToDoSchema.from_orm(todo) for todo in todos])


@app.get("/todos/{order_id}", name="단일 조회 api")
def get_todos_handler(order_id: int):
    ret = todo_data.get(order_id)
    if ret:
        return ret

    raise HTTPException(status_code=404, detail="todo not found")



class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos", name="입력 api")
def create_todo_handler(state: CreateTodoRequest):
    todo_data[state.id]  = state.dict()
    return todo_data[state.id]


# ------------9/10 학습 내용-------------

@app.patch("/todos/{todo_id}", status_code=200, name="수정 api")
def update_todo_handler(todo_id: int, is_done: bool = Body(..., embed=True)):
    todo = todo_data.get(todo_id)
    if todo:
        todo["is_done"] = is_done
        return todo

    raise HTTPException(status_code=404, detail="todo is not exist")



@app.delete("/todos", status_code=204, name="삭제 api")
def delete_todo_handler(todo_id: int):
    todo = todo_data.pop(todo_id, None)
    if todo:
        return

    raise HTTPException(status_code=404, detail="todo is not exist")