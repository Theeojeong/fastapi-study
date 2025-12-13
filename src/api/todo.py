from fastapi import APIRouter, Body, HTTPException, Depends
from typing import List

from database.repository import ToDoRepository, UserRepository
from database.orm import Todo, User
from schema.response import ListTodosResponse, TodoSchema
from schema.request import TodoRequestBody
from security import get_access_token
from service.user import UserService


router = APIRouter(prefix="/todos", tags=["Todo"])


# ===================GET======================
@router.get("")
def get_todos_handler(
    access_token: str = Depends(get_access_token),
    order: str | None = None,
    user_service: UserService = Depends(),
    user_repo: UserRepository = Depends()
):
    username: str = user_service.decode_jwt(access_token=access_token)

    user: User | None = user_repo.get_user_by_username(username=username)

    if not user:
        raise HTTPException(status_code=401, detail="User Not Found")

    todos: List[Todo] = user.todos

    if order == "DESC":
        return ListTodosResponse(
            todos=[TodoSchema.model_validate(ret) for ret in todos[::-1]]
        )
    return ListTodosResponse(todos=[TodoSchema.model_validate(ret) for ret in todos])


@router.get("/{todo_id}", status_code=200, name="todo 단일 조회")
def get_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if todo:
        return TodoSchema.model_validate(todo)
    raise HTTPException(status_code=400, detail="Todo Not Found")


# ===================POST======================
@router.post("")
def post_todo_handler(
    request: TodoRequestBody,
    todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: Todo = Todo.create(request=request)
    todo: Todo = todo_repo.create_todo(todo=todo)
    return TodoSchema.model_validate(todo)


# ===================PATCH======================


@router.patch("/{todo_id}", status_code=200)
def patch_todo_handler(
    todo_id: int,
    is_done: bool = Body(..., embed=True),
    todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: Todo | None = get_todo_by_todo_id(
        session=session,
        todo_id=todo_id,
    )
    if todo:
        todo.done() if is_done else todo.undone()
        todo = todo_repo.update_todo(todo=todo)
        return TodoSchema.model_validate(todo)

    raise HTTPException(status_code=404, detail="Todo Not Found")


# ===================DELETE======================
@router.delete("/{todo_id}", status_code=204)
def delete_todo_handler(
    todo_id: int,
    todo_repo: ToDoRepository = Depends(ToDoRepository),
):
    todo: Todo | None = todo_repo.get_todo_by_todo_id(todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo Not Found")

    todo_repo.delete_todo(todo_id=todo_id)
