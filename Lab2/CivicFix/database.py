import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, Session, create_engine

# Load environment variables from .env
load_dotenv()

# Create the database engine
engine = create_engine(
    os.environ["DATABASE_URL"],
    echo=True
)

# Create all database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Provide a database session
def get_session():
    with Session(engine) as session:
        yield session
