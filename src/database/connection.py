from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@localhost:3306/todos"

engine = create_engine(url=DATABASE_URL, echo=True) # conn
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False) # cursor

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()


# =============================================================================
# 📌 Raw SQL (pymysql) 대응 코드
# =============================================================================
#
# import pymysql
#
# # SQLAlchemy                          vs    Raw SQL (pymysql)
# # -------------------------------------------------------------------------
# # DATABASE_URL = "mysql+pymysql://..."      host, user, password, db 분리
# # engine = create_engine(...)         ≈     conn = pymysql.connect(...)
# # SessionFactory = sessionmaker(...)  ≈     커서를 만들기 위한 준비
# # session = SessionFactory()          ≈     cur = conn.cursor()
# # session.close()                     ≈     cur.close() + conn.close()
#
# # -------------------------------------------------------------------------
# # 동등한 Raw SQL 코드:
# # -------------------------------------------------------------------------
# # def get_db_raw():
# #     conn = pymysql.connect(
# #         host="localhost",
# #         user="root",
# #         password="fastapi",
# #         database="todos",
# #         cursorclass=pymysql.cursors.DictCursor
# #     )
# #     cur = conn.cursor()
# #     try:
# #         yield conn, cur  # API에서 conn, cur 사용
# #     finally:
# #         cur.close()
# #         conn.close()
# =============================================================================
