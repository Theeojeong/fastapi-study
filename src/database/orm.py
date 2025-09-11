from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import declarative_base
# sqlalchemy란 Python에서 가장 인기 있고 강력한 SQL 툴킷 및 ORM(Object-Relational Mapping) 라이브러리입니다.

Base = declarative_base()

class ToDo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    contents = Column(String(256), nullable=False)
    is_done = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"ToDo(id={self.id}, contents={self.contents}, is_done={self.is_done})"

