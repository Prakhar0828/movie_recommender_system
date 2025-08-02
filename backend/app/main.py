"""
Main FastAPI application for the movie recommendation system.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from .database.database import engine
from .database.models import Base
from .routers import movies, genres

# Create FastAPI app instance
app = FastAPI(
    title="Movie Recommendation System API",
    description="A simple API for movie recommendations based on genres",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],  # Streamlit default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(movies.router)
app.include_router(genres.router)


@app.on_event("startup")
async def startup_event():
    """
    Startup event to create database tables if they don't exist.
    """
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Error creating database tables: {e}")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: API information and available endpoints
    """
    return {
        "message": "Movie Recommendation System API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "movies": "/movies/",
            "genres": "/genres/",
            "movie_by_id": "/movies/{movie_id}",
            "movies_by_genre": "/movies/genre/{genre}",
            "search_movies": "/movies/search/?query={search_term}",
            "movies_by_year": "/movies/year/{start_year}/{end_year}",
            "movies_by_rating": "/movies/rating/{min_rating}"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy", "service": "movie-recommendation-api"}


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom exception handler for HTTP exceptions.
    
    Args:
        request: FastAPI request object
        exc: HTTPException instance
        
    Returns:
        JSONResponse: Formatted error response
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler for unexpected errors.
    
    Args:
        request: FastAPI request object
        exc: Exception instance
        
    Returns:
        JSONResponse: Formatted error response
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "status_code": 500
        }
    )


if __name__ == "__main__":
    """
    Run the FastAPI application using uvicorn.
    """
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
