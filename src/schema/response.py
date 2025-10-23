from pydantic import BaseModel, ConfigDict
from typing import List

class FastAPISchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    contents: str
    is_done: bool


class ListFastAPIResponse(BaseModel):
    fastapi: List[FastAPISchema]
