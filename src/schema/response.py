from pydantic import BaseModel, ConfigDict
from typing import List

class TodoSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    is_done: bool


class ListTodosResponse(BaseModel):
    todos: List[TodoSchema]
