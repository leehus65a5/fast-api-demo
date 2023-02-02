from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/vpi1"

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
metadata = MetaData()
metadata.reflect(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
        
# database = Database(DATABASE_URL)
# session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

