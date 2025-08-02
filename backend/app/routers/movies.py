"""
API router for movie-related endpoints in the movie recommendation system.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from typing import List

from ..database.database import get_database_session
from ..models.movie import Movie, MovieListResponse, GenreResponse
from ..services.movie_service import MovieService

# Create router instance
router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponse)
async def get_all_movies(database_session: Session = Depends(get_database_session)):
    """
    Get all movies from the database.
    
    Returns:
        MovieListResponse: List of all movies with total count
    """
    try:
        movies = MovieService.get_all_movies(database_session)
        return MovieListResponse(movies=movies, total=len(movies))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{movie_id}", response_model=Movie)
async def get_movie_by_id(
    movie_id: int, 
    database_session: Session = Depends(get_database_session)
):
    """
    Get a specific movie by its ID.
    
    Args:
        movie_id: Unique identifier of the movie
        database_session: Database session dependency
        
    Returns:
        Movie: Movie object if found
        
    Raises:
        HTTPException: 404 if movie not found, 422 if invalid ID
    """
    try:
        movie = MovieService.get_movie_by_id(database_session, movie_id)
        if not movie:
            raise HTTPException(
                status_code=404, 
                detail=f"Movie with ID {movie_id} not found"
            )
        return movie
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/genre/{genre}", response_model=MovieListResponse)
async def get_movies_by_genre(
    genre: str,
    limit: int = Query(default=8, ge=1, le=20, description="Maximum number of movies to return"),
    database_session: Session = Depends(get_database_session)
):
    """
    Get random movies from a specific genre.
    
    Args:
        genre: Genre to filter movies by
        limit: Maximum number of movies to return (1-20)
        database_session: Database session dependency
        
    Returns:
        MovieListResponse: List of random movies from the specified genre
        
    Raises:
        HTTPException: 404 if genre not found, 422 if invalid parameters
    """
    try:
        movies = MovieService.get_random_movies_by_genre(database_session, genre, limit)
        
        if not movies:
            raise HTTPException(
                status_code=404, 
                detail=f"No movies found for genre '{genre}'"
            )
        
        return MovieListResponse(movies=movies, total=len(movies))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/search/", response_model=MovieListResponse)
async def search_movies_by_title(
    query: str = Query(..., min_length=1, description="Search term for movie titles"),
    database_session: Session = Depends(get_database_session)
):
    """
    Search movies by title using case-insensitive partial matching.
    
    Args:
        query: Search term to match against movie titles
        database_session: Database session dependency
        
    Returns:
        MovieListResponse: List of movies matching the search term
    """
    try:
        movies = MovieService.search_movies_by_title(database_session, query)
        return MovieListResponse(movies=movies, total=len(movies))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/year/{start_year}/{end_year}", response_model=MovieListResponse)
async def get_movies_by_year_range(
    start_year: int,
    end_year: int,
    database_session: Session = Depends(get_database_session)
):
    """
    Get movies within a specific year range.
    
    Args:
        start_year: Start year for the range
        end_year: End year for the range
        database_session: Database session dependency
        
    Returns:
        MovieListResponse: List of movies within the year range
        
    Raises:
        HTTPException: 422 if invalid year range
    """
    try:
        if start_year > end_year:
            raise HTTPException(
                status_code=422, 
                detail="Start year must be less than or equal to end year"
            )
        
        movies = MovieService.get_movies_by_year_range(database_session, start_year, end_year)
        return MovieListResponse(movies=movies, total=len(movies))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/rating/{min_rating}", response_model=MovieListResponse)
async def get_movies_by_rating_threshold(
    min_rating: float = Path(..., ge=0.0, le=10.0, description="Minimum rating threshold"),
    database_session: Session = Depends(get_database_session)
):
    """
    Get movies with rating above a certain threshold.
    
    Args:
        min_rating: Minimum rating threshold (0.0-10.0)
        database_session: Database session dependency
        
    Returns:
        MovieListResponse: List of movies above the rating threshold
    """
    try:
        movies = MovieService.get_movies_by_rating_threshold(database_session, min_rating)
        return MovieListResponse(movies=movies, total=len(movies))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
