from fastapi import FastAPI
from api.todo import router as todo_router
from api.user import router as user_router

app = FastAPI()

app.include_router(todo_router)
app.include_router(user_router)

@app.get("/")
def health_check_handler():
    return {"Hi": "HelloWorld"}
