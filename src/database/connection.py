from sqlalchemy import create_engine # -> 데이터베이스 연결을 관리하는 엔진 생성
from sqlalchemy.orm import sessionmaker # -> 데이터베이스 세션을 생성하는 팩토리 클래스

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3306/todos"

engine = create_engine(url=DATABASE_URL, echo=True)
# 데이터베이스 연결 풀 관리
# 연결 재사용(성능 향상)
# SQL 방언 처리(MYSQL 문법)
 
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
# 세션 인스턴스 생성 도구
# 트랜잭션 관리
# ORM 쿼리 실행

# ------python console에서 db 연결 test------------

# from database.connection import SessionFactory 
# session = SessionFactory()
# from sqlalchemy import select
# session.scalar(select(1))
# 1이 출력된다면 연결 테스트 성공