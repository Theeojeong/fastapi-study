from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Boolean, String, Column, ForeignKey
from schema.request import TodoRequestBody

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"FastAPI(id={self.id}, contents={self.contents}, is_bool={self.is_done}"

    @classmethod
    def create(cls, request: TodoRequestBody) -> "Todo":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )

    def done(self) -> "Todo":
        self.is_done = True
        return self

    def undone(self) -> "Todo":
        self.is_done = False
        return self

class User(Base):
    __tablename__ ="user"

    id = Column(Integer, primary_key=True)
    username = Column(String(256), nullable=False)
    password = Column(String(256), nullable=False)
