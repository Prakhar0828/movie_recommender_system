"""
SQLAlchemy ORM models for the movie recommendation system.
"""
from sqlalchemy import Column, Integer, String, Float, Text, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Movie(Base):
    """
    Movie model representing the movies table in the database.
    
    Attributes:
        id: Primary key, unique movie identifier
        title: Movie title (indexed for search)
        year: Release year
        genre: Movie genre (indexed for filtering)
        rating: IMDb/rating score (0-10)
        director: Movie director
        cast: JSON string of cast members
        plot: Movie plot summary
    """
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    year = Column(Integer)
    genre = Column(String(100), index=True)
    rating = Column(Float)
    director = Column(String(255))
    cast = Column(Text)  # JSON string for simplicity
    plot = Column(Text)
    
    # Create indexes for better query performance
    __table_args__ = (
        Index('idx_genre', 'genre'),
        Index('idx_title', 'title'),
        Index('idx_year', 'year'),
    )
