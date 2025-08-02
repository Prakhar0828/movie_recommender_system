"""
API router for genre-related endpoints in the movie recommendation system.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_database_session
from ..models.movie import GenreResponse
from ..services.movie_service import MovieService

# Create router instance
router = APIRouter(prefix="/genres", tags=["genres"])


@router.get("/", response_model=GenreResponse)
async def get_all_genres(database_session: Session = Depends(get_database_session)):
    """
    Get all available genres from the database.
    
    Returns:
        GenreResponse: List of all unique genres
    """
    try:
        genres = MovieService.get_all_genres(database_session)
        return GenreResponse(genres=genres)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}") 