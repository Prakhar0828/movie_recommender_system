"""
Business logic layer for movie operations in the movie recommendation system.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import random

from ..database.models import Movie


class MovieService:
    """
    Service class containing business logic for movie operations.
    """
    
    @staticmethod
    def get_all_movies(database_session: Session) -> List[Movie]:
        """
        Retrieve all movies from the database.
        
        Args:
            database_session: SQLAlchemy database session
            
        Returns:
            List[Movie]: List of all movies in the database
        """
        return database_session.query(Movie).all()
    
    @staticmethod
    def get_movie_by_id(database_session: Session, movie_id: int) -> Optional[Movie]:
        """
        Retrieve a specific movie by its ID.
        
        Args:
            database_session: SQLAlchemy database session
            movie_id: Unique identifier of the movie
            
        Returns:
            Optional[Movie]: Movie object if found, None otherwise
        """
        return database_session.query(Movie).filter(Movie.id == movie_id).first()
    
    @staticmethod
    def get_random_movies_by_genre(
        database_session: Session, 
        genre: str, 
        limit: int = 8
    ) -> List[Movie]:
        """
        Get random movies from a specific genre.
        
        Args:
            database_session: SQLAlchemy database session
            genre: Genre to filter movies by
            limit: Maximum number of movies to return (default: 8)
            
        Returns:
            List[Movie]: List of random movies from the specified genre
        """
        movies = database_session.query(Movie).filter(Movie.genre == genre).all()
        
        if not movies:
            return []
        
        # If we have fewer movies than the limit, return all
        if len(movies) <= limit:
            return movies
        
        # Return random selection of movies
        return random.sample(movies, limit)
    
    @staticmethod
    def get_all_genres(database_session: Session) -> List[str]:
        """
        Retrieve all unique genres from the database.
        
        Args:
            database_session: SQLAlchemy database session
            
        Returns:
            List[str]: List of all unique genres
        """
        genres = database_session.query(Movie.genre).distinct().all()
        return [genre[0] for genre in genres if genre[0]]
    
    @staticmethod
    def get_movies_by_year_range(
        database_session: Session, 
        start_year: int, 
        end_year: int
    ) -> List[Movie]:
        """
        Get movies within a specific year range.
        
        Args:
            database_session: SQLAlchemy database session
            start_year: Start year for the range
            end_year: End year for the range
            
        Returns:
            List[Movie]: List of movies within the year range
        """
        return database_session.query(Movie).filter(
            Movie.year >= start_year,
            Movie.year <= end_year
        ).all()
    
    @staticmethod
    def get_movies_by_rating_threshold(
        database_session: Session, 
        min_rating: float
    ) -> List[Movie]:
        """
        Get movies with rating above a certain threshold.
        
        Args:
            database_session: SQLAlchemy database session
            min_rating: Minimum rating threshold
            
        Returns:
            List[Movie]: List of movies above the rating threshold
        """
        return database_session.query(Movie).filter(
            Movie.rating >= min_rating
        ).all()
    
    @staticmethod
    def search_movies_by_title(
        database_session: Session, 
        search_term: str
    ) -> List[Movie]:
        """
        Search movies by title using case-insensitive partial matching.
        
        Args:
            database_session: SQLAlchemy database session
            search_term: Search term to match against movie titles
            
        Returns:
            List[Movie]: List of movies matching the search term
        """
        return database_session.query(Movie).filter(
            Movie.title.ilike(f"%{search_term}%")
        ).all()
