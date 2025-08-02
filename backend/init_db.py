"""
Database initialization script for the movie recommendation system.
"""
import sys
import os


from app.database.database import engine, SessionLocal
from app.database.models import Base
from app.utils.data_seeder import seed_database


def init_database():
    """
    Initialize the database by creating tables and seeding with sample data.
    """
    try:
        print("Creating database tables...")
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
        
        # Seed the database with sample data
        print("Seeding database with sample movies...")
        database_session = SessionLocal()
        try:
            seed_database(database_session)
            print("Database initialization completed successfully!")
        finally:
            database_session.close()
            
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    """
    Run the database initialization script.
    """
    print("Starting database initialization...")
    init_database()
    print("Database initialization finished!")
