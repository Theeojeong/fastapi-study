from fastapi import FastAPI
from api.todo import router as todo_router

app = FastAPI()

app.include_router(todo_router)


@app.get("/")
def health_check_handler():
    return {"Hi": "HelloWorld"}
