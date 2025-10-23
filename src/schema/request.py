from pydantic import BaseModel

class TodoRequestBody(BaseModel):
    contents: str
    is_done: bool
