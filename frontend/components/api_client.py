"""
Mock API client for the movie recommendation frontend.
This will be replaced with real HTTP requests when integrating with the backend.
"""
import json
from typing import List, Dict, Any, Optional


class MockMovieAPI:
    """
    Mock API client that simulates backend responses.
    """
    
    def __init__(self):
        """Initialize the mock API with sample data."""
        self.sample_movies = self._load_sample_data()
    
    def _load_sample_data(self) -> List[Dict[str, Any]]:
        """
        Load sample movie data for demonstration.
        
        Returns:
            List[Dict]: Sample movie data
        """
        return [
            {
                "id": 1,
                "title": "The Dark Knight",
                "year": 2008,
                "genre": "Action",
                "rating": 9.0,
                "director": "Christopher Nolan",
                "cast": json.dumps(["Christian Bale", "Heath Ledger", "Aaron Eckhart"]),
                "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
            },
            {
                "id": 2,
                "title": "Inception",
                "year": 2010,
                "genre": "Sci-Fi",
                "rating": 8.8,
                "director": "Christopher Nolan",
                "cast": json.dumps(["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"]),
                "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
            },
            {
                "id": 3,
                "title": "The Shawshank Redemption",
                "year": 1994,
                "genre": "Drama",
                "rating": 9.3,
                "director": "Frank Darabont",
                "cast": json.dumps(["Tim Robbins", "Morgan Freeman", "Bob Gunton"]),
                "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
            },
            {
                "id": 4,
                "title": "The Grand Budapest Hotel",
                "year": 2014,
                "genre": "Comedy",
                "rating": 8.1,
                "director": "Wes Anderson",
                "cast": json.dumps(["Ralph Fiennes", "Tony Revolori", "F. Murray Abraham"]),
                "plot": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge."
            },
            {
                "id": 5,
                "title": "The Shining",
                "year": 1980,
                "genre": "Horror",
                "rating": 8.4,
                "director": "Stanley Kubrick",
                "cast": json.dumps(["Jack Nicholson", "Shelley Duvall", "Danny Lloyd"]),
                "plot": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future."
            },
            {
                "id": 6,
                "title": "Gone Girl",
                "year": 2014,
                "genre": "Thriller",
                "rating": 8.1,
                "director": "David Fincher",
                "cast": json.dumps(["Ben Affleck", "Rosamund Pike", "Neil Patrick Harris"]),
                "plot": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent."
            }
        ]
    
    def get_all_movies(self) -> List[Dict[str, Any]]:
        """
        Get all movies from the mock database.
        
        Returns:
            List[Dict]: List of all movies
        """
        return self.sample_movies.copy()
    
    def get_movie_by_id(self, movie_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific movie by ID.
        
        Args:
            movie_id: Unique identifier of the movie
            
        Returns:
            Optional[Dict]: Movie object if found, None otherwise
        """
        for movie in self.sample_movies:
            if movie['id'] == movie_id:
                return movie
        return None
    
    def get_movies_by_genre(self, genre: str, limit: int = 8) -> List[Dict[str, Any]]:
        """
        Get random movies from a specific genre.
        
        Args:
            genre: Genre to filter movies by
            limit: Maximum number of movies to return
            
        Returns:
            List[Dict]: List of movies from the specified genre
        """
        genre_movies = [movie for movie in self.sample_movies if movie['genre'].lower() == genre.lower()]
        
        if len(genre_movies) <= limit:
            return genre_movies
        
        # Simple random selection (in real implementation, this would be more sophisticated)
        import random
        return random.sample(genre_movies, limit)
    
    def get_all_genres(self) -> List[str]:
        """
        Get all available genres.
        
        Returns:
            List[str]: List of all unique genres
        """
        genres = set(movie['genre'] for movie in self.sample_movies)
        return sorted(list(genres))
    
    def search_movies_by_title(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Search movies by title using case-insensitive partial matching.
        
        Args:
            search_term: Search term to match against movie titles
            
        Returns:
            List[Dict]: List of movies matching the search term
        """
        search_term_lower = search_term.lower()
        matching_movies = []
        
        for movie in self.sample_movies:
            if search_term_lower in movie['title'].lower():
                matching_movies.append(movie)
        
        return matching_movies
    
    def get_movies_by_year_range(self, start_year: int, end_year: int) -> List[Dict[str, Any]]:
        """
        Get movies within a specific year range.
        
        Args:
            start_year: Start year for the range
            end_year: End year for the range
            
        Returns:
            List[Dict]: List of movies within the year range
        """
        return [
            movie for movie in self.sample_movies 
            if movie['year'] and start_year <= movie['year'] <= end_year
        ]
    
    def get_movies_by_rating_threshold(self, min_rating: float) -> List[Dict[str, Any]]:
        """
        Get movies with rating above a certain threshold.
        
        Args:
            min_rating: Minimum rating threshold
            
        Returns:
            List[Dict]: List of movies above the rating threshold
        """
        return [
            movie for movie in self.sample_movies 
            if movie['rating'] and movie['rating'] >= min_rating
        ]


# Global instance for use across the application
movie_api = MockMovieAPI()
