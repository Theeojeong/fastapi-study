from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, Boolean, String, Column, ForeignKey
from schema.request import TodoRequestBody

Base = declarative_base()

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)           # id INT PRIMARY KEY AUTO_INCREMENT
    contents = Column(String(256), nullable=False)   # contents VARCHAR(256) NOT NULL
    is_done = Column(Boolean, nullable=False)        # is_done BOOLEAN NOT NULL
    user_id = Column(Integer, ForeignKey("user.id")) # user_id INT, FOREIGN KEY (user_id) REFERENCES user(id)

    def __repr__(self) -> str:
        return f"FastAPI(id={self.id}, contents={self.contents}, is_bool={self.is_done}"

    @classmethod
    def create(cls, request: TodoRequestBody) -> "Todo":
        return cls(
            contents=request.contents,
            is_done=request.is_done
        )
        # Raw SQL에서는 이런 팩토리 메서드 없이 바로 INSERT:
        # cur.execute("INSERT INTO todos (contents, is_done) VALUES (%s, %s)",
        #             (request.contents, request.is_done))

    def done(self) -> "Todo":
        self.is_done = True
        return self
        # Raw SQL: cur.execute("UPDATE todos SET is_done = TRUE WHERE id = %s", (self.id,))

    def undone(self) -> "Todo":
        self.is_done = False
        return self
        # Raw SQL: cur.execute("UPDATE todos SET is_done = FALSE WHERE id = %s", (self.id,))

class User(Base):
    __tablename__ ="user"

    id = Column(Integer, primary_key=True)            # id INT PRIMARY KEY AUTO_INCREMENT
    username = Column(String(256), nullable=False)    # username VARCHAR(256) NOT NULL
    password = Column(String(256), nullable=False)    # password VARCHAR(256) NOT NULL


# =============================================================================
# 📌 ORM 클래스 = SQL CREATE TABLE 문
# =============================================================================
#
# class Todo(Base) 는 아래 SQL과 동일합니다:
#
# CREATE TABLE todos (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     contents VARCHAR(256) NOT NULL,
#     is_done BOOLEAN NOT NULL,
#     user_id INT,
#     FOREIGN KEY (user_id) REFERENCES user(id)
# );
#
# -------------------------------------------------------------------------
#
# class User(Base) 는 아래 SQL과 동일합니다:
#
# CREATE TABLE user (
#     id INT PRIMARY KEY AUTO_INCREMENT,
#     username VARCHAR(256) NOT NULL,
#     password VARCHAR(256) NOT NULL
# );
#
# =============================================================================
# 📌 ORM 객체 vs Raw SQL 딕셔너리
# =============================================================================
#
# ORM 방식:
#   todo = Todo(contents="할일", is_done=False)
#   print(todo.contents)  # "할일"
#
# Raw SQL 방식 (DictCursor 사용 시):
#   cur.execute("SELECT * FROM todos WHERE id = 1")
#   todo = cur.fetchone()  # {'id': 1, 'contents': '할일', 'is_done': False}
#   print(todo['contents'])  # "할일"
#
# =============================================================================
