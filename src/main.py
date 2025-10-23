from fastapi import FastAPI, Body, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import get_db
from database.repository import get_fastapi
from database.orm import fastapi
from schema.response import ListFastAPIResponse, FastAPISchema
from typing import List

app = FastAPI()


@app.get("/")
def health_check_handler():
    return {"HelloWorld"}


@app.get("/fastapi")
def get_todos_handler(
    order: str | None = None,
    session: Session = Depends(get_db),
):
    rets: List[fastapi] = get_fastapi(session=session)


    if order == "DESC":
        return ListFastAPIResponse(
            fastapi=[FastAPISchema.model_validate(ret) for ret in rets[::-1]]
        )

    return ListFastAPIResponse(
        fastapi=[FastAPISchema.model_validate(ret) for ret in rets]
    )


@app.get("/todo/{todo_id}", status_code=200, name="todo 단일 조회")
def get_todo_handler(todo_id: int):
    result = todo_data.get(todo_id, {})
    if result:
        return result
    raise HTTPException(status_code=400, detail="Todo Not Found")


class TodoRequestBody(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos")
def post_todo_handler(order: TodoRequestBody):
    todo_data[order.id] = order.model_dump()
    return todo_data[order.id]


@app.patch("/todos")
def patch_todo_handler(num: int, is_done: bool = Body(..., embed=True)):

    todo = todo_data.get(num)

    if todo:
        todo["is_done"] = is_done
        return todo
    return {}


@app.delete("/todos")
def delete_todo_handler(id: int):

    todo_data.pop(id, None)

    return todo_data
