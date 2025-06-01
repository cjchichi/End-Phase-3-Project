
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
#engine = create_engine("sqlite:///your_database_name.db", echo=True)

DATABASE_URL = "sqlite:///../expenses.db" 
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def init_db():
    import lib.models.expense, lib.models.user, lib.models.category 
    Base.metadata.create_all(bind=engine)
