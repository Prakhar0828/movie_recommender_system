"""
Database configuration and connection setup for the movie recommendation system.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./movies.db"

# Create SQLite engine with check_same_thread=False for async compatibility
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()


def get_database_session():
    """
    Dependency function to get database session.
    
    Yields:
        Session: SQLAlchemy database session
    """
    database_session = SessionLocal()
    try:
        yield database_session
    finally:
        database_session.close()
