"""
Helper functions for the movie recommendation frontend.
"""
import json
from typing import List, Dict, Any


def format_movie_data(movie: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format movie data for display in the frontend.
    
    Args:
        movie: Raw movie data dictionary
        
    Returns:
        Dict: Formatted movie data
    """
    formatted_movie = movie.copy()
    
    # Format cast from JSON string to list
    if movie.get('cast') and isinstance(movie['cast'], str):
        try:
            formatted_movie['cast'] = json.loads(movie['cast'])
        except json.JSONDecodeError:
            formatted_movie['cast'] = [movie['cast']]
    
    # Ensure cast is always a list
    if not isinstance(formatted_movie.get('cast'), list):
        formatted_movie['cast'] = []
    
    # Format rating to 1 decimal place
    if movie.get('rating'):
        formatted_movie['rating'] = round(float(movie['rating']), 1)
    
    return formatted_movie


def format_cast_display(cast: List[str]) -> str:
    """
    Format cast list for display.
    
    Args:
        cast: List of cast members
        
    Returns:
        str: Formatted cast string
    """
    if not cast:
        return "Cast information not available"
    
    if len(cast) <= 3:
        return ", ".join(cast)
    else:
        return ", ".join(cast[:3]) + f" and {len(cast) - 3} more"


def get_genre_colors() -> Dict[str, str]:
    """
    Get color scheme for different genres.
    
    Returns:
        Dict: Genre to color mapping
    """
    return {
        "Action": "#FF6B6B",
        "Comedy": "#4ECDC4", 
        "Drama": "#45B7D1",
        "Horror": "#96CEB4",
        "Sci-Fi": "#FFEAA7",
        "Thriller": "#DDA0DD"
    }


def get_genre_emoji(genre: str) -> str:
    """
    Get emoji for different genres.
    
    Args:
        genre: Movie genre
        
    Returns:
        str: Emoji for the genre
    """
    emoji_map = {
        "Action": "💥",
        "Comedy": "😂",
        "Drama": "🎭",
        "Horror": "👻",
        "Sci-Fi": "🚀",
        "Thriller": "😱"
    }
    return emoji_map.get(genre, "🎬")


def validate_year_range(start_year: int, end_year: int) -> bool:
    """
    Validate year range input.
    
    Args:
        start_year: Start year
        end_year: End year
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 1888 <= start_year <= 2030 and 1888 <= end_year <= 2030 and start_year <= end_year


def validate_rating(rating: float) -> bool:
    """
    Validate rating input.
    
    Args:
        rating: Rating value
        
    Returns:
        bool: True if valid, False otherwise
    """
    return 0.0 <= rating <= 10.0
