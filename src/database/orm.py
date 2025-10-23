from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Boolean, String, Column
from schema import request
from schema.request import TodoRequestBody

Base = declarative_base()

class fastapi(Base):
    __tablename__ = "fastapi"

    id = Column(Integer, primary_key=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"FastAPI(id={self.id}, contents={self.contents}, is_bool={self.is_done}"

    @classmethod
    def create(cls, request: TodoRequestBody) -> "fastapi":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )
    
    def done(self) -> "fastapi":
        self.is_done = True
        return self

    def undone(self) -> "fastapi":
        self.is_done = False
        return self
