"""
Pydantic models for API request/response validation in the movie recommendation system.
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class MovieBase(BaseModel):
    """
    Base Pydantic model for movie data validation.
    
    Attributes:
        title: Movie title
        year: Release year
        genre: Movie genre
        rating: IMDb/rating score
        director: Movie director
        cast: Cast members as JSON string
        plot: Movie plot summary
    """
    title: str = Field(..., min_length=1, max_length=255, description="Movie title")
    year: Optional[int] = Field(None, ge=1888, le=2030, description="Release year")
    genre: Optional[str] = Field(None, max_length=100, description="Movie genre")
    rating: Optional[float] = Field(None, ge=0.0, le=10.0, description="Rating score (0-10)")
    director: Optional[str] = Field(None, max_length=255, description="Movie director")
    cast: Optional[str] = Field(None, description="Cast members as JSON string")
    plot: Optional[str] = Field(None, description="Movie plot summary")


class Movie(MovieBase):
    """
    Pydantic model for movie response including the ID.
    
    Attributes:
        id: Unique movie identifier
    """
    id: int = Field(..., description="Unique movie identifier")
    
    class Config:
        """Pydantic configuration for ORM compatibility."""
        from_attributes = True


class MovieListResponse(BaseModel):
    """
    Pydantic model for movie list API responses.
    
    Attributes:
        movies: List of movies
        total: Total number of movies in the response
    """
    movies: List[Movie] = Field(..., description="List of movies")
    total: int = Field(..., ge=0, description="Total number of movies")


class GenreResponse(BaseModel):
    """
    Pydantic model for genre list API responses.
    
    Attributes:
        genres: List of available genres
    """
    genres: List[str] = Field(..., description="List of available genres")
