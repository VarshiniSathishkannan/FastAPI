from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = 'postgresql://postgres:123@localhost/fastapi_backend'

engine = create_engine(SQLALCHEMY_DB_URL)

Sessionlocal = sessionmaker(autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()