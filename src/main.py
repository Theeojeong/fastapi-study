from fastapi import FastAPI, Body, HTTPException, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.connection import get_db
from database.repository import (
    get_fastapi,
    get_fastapi_by_fastapi_id,
    fastapi_create,
    fastapi_update,
    fastapi_delete,
)
from database.orm import fastapi
from schema.response import ListFastAPIResponse, FastAPISchema
from schema.request import TodoRequestBody
from typing import List

app = FastAPI()

# ===================GET======================


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


@app.get("/todo/{fastapi_id}", status_code=200, name="fastapi 단일 조회")
def get_todo_handler(
    fastapi_id: int,
    session: Session = Depends(get_db),
):
    ret: fastapi | None = get_fastapi_by_fastapi_id(
        session=session, fastapi_id=fastapi_id
    )

    if ret:
        return FastAPISchema.model_validate(ret)
    raise HTTPException(status_code=400, detail="Todo Not Found")


# ===================POST======================


@app.post("/todos")
def post_todo_handler(
    request: TodoRequestBody,
    session: Session = Depends(get_db),
):
    ret: fastapi = fastapi.create(request=request)
    ret = fastapi_create(session=session, fastapi=ret)
    return FastAPISchema.model_validate(ret)


# ===================PATCH======================


@app.patch("/todo/{fastapi_id}", status_code=200)
def patch_todo_handler(
    fastapi_id: int,
    is_done: bool = Body(..., embed=True),
    session: Session = Depends(get_db),
):
    ret: fastapi | None = get_fastapi_by_fastapi_id(
        session=session, fastapi_id=fastapi_id,
    )
    if ret:
        ret.done() if is_done else ret.undone()
        ret = fastapi_update(session=session, fastapi=ret)
        return FastAPISchema.model_validate(ret)

    raise HTTPException(status_code=404, detail="Todo Not Found")


# ===================DELEET======================


@app.delete("/todo/{fastapi_id}")
def delete_todo_handler(fastapi_id: int, session: Session = Depends(get_db),):

    ret: fastapi | None = get_fastapi_by_fastapi_id(session=session, fastapi_id=fastapi_id,)
    if not ret:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    fastapi_delete(session=session, fastapi_id=fastapi_id)
