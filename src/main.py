from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def health_check_handler():
    return {"helloworld"}


todo_data = {

    1: {
        "id": 1,
        "contents": "one",
        "is_done": True
    },
    
    2: {
        "id": 2,
        "contents": "two",
        "is_done": False
    },
    
    3: {
        "id": 3,
        "contents": "three",
        "is_done": False
    }

}

@app.get("/todos")
def get_todos_hanlder(order: str | None = None):

    ret = list(todo_data.values())

    if order and order == "DESC":
        return ret[::-1]

    return ret

@app.get("/todos/{todo_id}")
def get_todo_handler(todo_id: int):
    return todo_data.get(todo_id, {})


class CreateTodoRequest(BaseModel):
    id: int
    contents: str
    is_done: bool


@app.post("/todos")
def create_todo_handler(request: CreateTodoRequest):
    todo_data[request.id] = request.dict()
    return todo_data[request.id]

