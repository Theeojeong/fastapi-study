from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:fastapi@localhost:3306/todos"

engine = create_engine(url=DATABASE_URL, echo=True)
SessionFactory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
