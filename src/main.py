# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# @app.get("/")
# def health_check_handler():
#     return {"helloworld"}


# todo_data = {

#     1: {
#         "id": 1,
#         "contents": "one",
#         "is_done": True
#     },
    
#     2: {
#         "id": 2,
#         "contents": "two",
#         "is_done": False
#     },
    
#     3: {
#         "id": 3,
#         "contents": "three",
#         "is_done": False
#     }

# }

# @app.get("/todos")
# def get_todos_hanlder(order: str | None = None):

#     ret = list(todo_data.values())

#     if order and order == "DESC":
#         return ret[::-1]

#     return ret

# @app.get("/todos/{todo_id}")
# def get_todo_handler(todo_id: int):
#     return todo_data.get(todo_id, {})


# class CreateTodoRequest(BaseModel):
#     id: int
#     contents: str
#     is_done: bool


# @app.post("/todos")
# def create_todo_handler(request: CreateTodoRequest):
#     todo_data[request.id] = request.dict()
#     return todo_data[request.id]



# ------------9/9 학습 내용-------------

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check():
    return {"helloworld"}

todo_data = {
    1: {
        "id": 1,
        "contents": "오늘",
        "is_done": True
    },

    2: {
        "id": 2,
        "contents": "내일",
        "is_done": True
    },

    3: {
        "id": 3,
        "contents": "모레",
        "is_done": False
    }
}


@app.get("/todos", name="전체 조회 api")
def get_todos_handler(order: str | None = None):
    ret = list(todo_data.values())
    if order == "up":
        return ret[::-1]

    return ret


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