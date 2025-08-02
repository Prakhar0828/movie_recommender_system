"""
Real API client for the movie recommendation frontend.
Connects to the deployed FastAPI backend on Render.
"""
import requests
import streamlit as st
from typing import List, Dict, Any, Optional


class MovieAPI:
    """
    Real API client that connects to the deployed FastAPI backend.
    """
    
    def __init__(self, base_url: str = "https://movie-recommender-system-gvq5.onrender.com"):
        """
        Initialize the API client with the backend URL.
        
        Args:
            base_url: Base URL of the deployed backend
        """
        self.base_url = base_url.rstrip('/')
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make HTTP request to the backend API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            Optional[Dict]: Response data or None if error
        """
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")
            return None
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            return None
    
    def get_all_movies(self) -> List[Dict[str, Any]]:
        """
        Get all movies from the backend API.
        
        Returns:
            List[Dict]: List of all movies
        """
        response_data = self._make_request("/movies/")
        if response_data and "movies" in response_data:
            return response_data["movies"]
        return []
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific movie by ID from the backend API.
        
        Args:
            movie_id: Unique identifier of the movie
            
        Returns:
            Optional[Dict]: Movie object if found, None otherwise
        """
        return self._make_request(f"/movies/{movie_id}")
    
    def get_movies_by_genre(self, genre: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Get random movies from a specific genre from the backend API.
        
        Args:
            genre: Genre to filter movies by
            limit: Maximum number of movies to return
            
        Returns:
            List[Dict]: List of movies from the specified genre
        """
        params = {"limit": limit}
        response_data = self._make_request(f"/movies/genre/{genre}", params)
        if response_data and "movies" in response_data:
            return response_data["movies"]
        return []
    
    def get_all_genres(self) -> List[str]:
        """
        Get all available genres from the backend API.
        
        Returns:
            List[str]: List of all unique genres
        """
        response_data = self._make_request("/genres/")
        if response_data and "genres" in response_data:
            return response_data["genres"]
        return []
    
    def search_movies_by_title(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search movies by title using the backend API.
        
        Args:
            search_term: Search term to match against movie titles
            
        Returns:
            List[Dict]: List of movies matching the search term
        """
        params = {"query": search_term}
        response_data = self._make_request("/movies/search/", params)
        if response_data and "movies" in response_data:
            return response_data["movies"]
        return []
    
    def get_movies_by_year_range(self, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """
        Get movies within a specific year range from the backend API.
        
        Args:
            start_year: Start year for the range
            end_year: End year for the range
            
        Returns:
            List[Dict]: List of movies within the year range
        """
        response_data = self._make_request(f"/movies/year/{start_year}/{end_year}")
        if response_data and "movies" in response_data:
            return response_data["movies"]
        return []
    
    def get_movies_by_rating_threshold(self, min_rating: float) -> List[Dict[str, Any]]:
        """
        Get movies with rating above a certain threshold from the backend API.
        
        Args:
            min_rating: Minimum rating threshold
            
        Returns:
            List[Dict]: List of movies above the rating threshold
        """
        response_data = self._make_request(f"/movies/rating/{min_rating}")
        if response_data and "movies" in response_data:
            return response_data["movies"]
        return []
    
    def test_connection(self) -> bool:
        """
        Test the connection to the backend API.
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Try the health endpoint first
            response = requests.get(f"{self.base_url}/health", timeout=10)
            if response.status_code == 200:
                return True
            
            # If health endpoint doesn't work, try the root endpoint
            response = requests.get(f"{self.base_url}/", timeout=10)
            return response.status_code == 200
            
        except requests.exceptions.Timeout:
            st.error("Connection timeout - backend might be slow to respond")
            return False
        except requests.exceptions.ConnectionError:
            st.error("Connection error - backend might be down or URL is incorrect")
            return False
        except Exception as e:
            st.error(f"Connection test error: {e}")
            return False


# Global instance for use across the application
movie_api = MovieAPI()
