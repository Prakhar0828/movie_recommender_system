"""
Genre recommendations page for the movie recommendation frontend.
Allows users to select a genre and get random movie suggestions.
"""
import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.api_client import movie_api
from components.movie_card import display_movie_grid
from utils.helpers import format_movie_data, get_genre_emoji


def show_genre_recommendations():
    """
    Display the genre recommendations page.
    """
    try:
        st.title("🎯 Genre Recommendations")
        st.markdown("Select a genre to get personalized movie recommendations!")
        
        # Debug: Show backend URL
        st.info(f"Connecting to backend: {movie_api.base_url}")
        
        # Check backend connection with better error handling
        try:
            connection_status = movie_api.test_connection()
            st.write(f"Connection status: {connection_status}")
            
            if not connection_status:
                st.error("⚠️ Cannot connect to the backend API. Please check your connection and try again.")
                st.info("Backend URL: " + movie_api.base_url)
                
                # Show more debugging info
                st.subheader("🔧 Debug Information")
                st.write("Trying to test connection...")
                try:
                    import requests
                    response = requests.get(f"{movie_api.base_url}/health", timeout=5)
                    st.write(f"Health check response: {response.status_code}")
                    st.write(f"Response content: {response.text}")
                except Exception as e:
                    st.write(f"Health check error: {e}")
                
                return
        except Exception as e:
            st.error(f"Error testing connection: {e}")
            return
        
        # Get available genres with loading state and error handling
        try:
            with st.spinner("Loading genres..."):
                genres = movie_api.get_all_genres()
            
            st.write(f"Genres loaded: {genres}")
            
            if not genres:
                st.warning("No genres found. The backend might be empty or there was an error loading data.")
                
                # Try to get all movies to see if there's data
                st.write("Trying to get all movies...")
                all_movies = movie_api.get_all_movies()
                st.write(f"Total movies found: {len(all_movies) if all_movies else 0}")
                
                if all_movies:
                    # Extract genres from movies
                    movie_genres = list(set([movie.get('genre') for movie in all_movies if movie.get('genre')]))
                    st.write(f"Genres from movies: {movie_genres}")
                    genres = movie_genres
                else:
                    return
        except Exception as e:
            st.error(f"Error loading genres: {e}")
            return
        
        # Genre selection
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_genre = st.selectbox(
                "Choose a genre",
                genres,
                index=0,
                help="Select a genre to get movie recommendations"
            )
        
        with col2:
            limit = st.number_input(
                "Number of recommendations",
                min_value=1,
                max_value=20,
                value=8,
                help="How many movies to recommend"
            )
        
        # Get recommendations button
        if st.button("🎲 Get Recommendations", type="primary"):
            if selected_genre:
                # Get movies by genre with loading state
                try:
                    with st.spinner(f"Getting {selected_genre} recommendations..."):
                        recommended_movies = movie_api.get_movies_by_genre(selected_genre, limit)
                    
                    st.write(f"Movies found: {len(recommended_movies) if recommended_movies else 0}")
                    
                    if recommended_movies:
                        st.success(f"🎉 Found {len(recommended_movies)} movies in {selected_genre}!")
                        
                        # Display genre info
                        genre_emoji = get_genre_emoji(selected_genre)
                        st.markdown(f"### {genre_emoji} {selected_genre} Movies")
                        
                        # Format movies for display
                        formatted_movies = [format_movie_data(movie) for movie in recommended_movies]
                        
                        # Display options
                        col1, col2 = st.columns([1, 4])
                        with col1:
                            show_details = st.checkbox("Show Details", value=True)
                        with col2:
                            columns = st.selectbox("Columns", [2, 3, 4], index=1)
                        
                        # Display movies in grid
                        display_movie_grid(formatted_movies, columns=columns, show_details=show_details)
                        
                        # Get new recommendations button
                        if st.button("🔄 Get New Recommendations"):
                            st.rerun()
                        
                        # Movie statistics for this genre
                        st.markdown("---")
                        st.subheader(f"📊 {selected_genre} Statistics")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            movies_with_rating = [m for m in recommended_movies if m['rating']]
                            if movies_with_rating:
                                avg_rating = sum(m['rating'] for m in movies_with_rating) / len(movies_with_rating)
                                st.metric("Average Rating", f"{avg_rating:.1f}/10")
                            else:
                                st.metric("Average Rating", "N/A")
                        
                        with col2:
                            movies_with_year = [m for m in recommended_movies if m['year']]
                            if movies_with_year:
                                year_range = f"{min(m['year'] for m in movies_with_year)} - {max(m['year'] for m in movies_with_year)}"
                                st.metric("Year Range", year_range)
                            else:
                                st.metric("Year Range", "N/A")
                        
                        with col3:
                            movies_with_rating = [m for m in recommended_movies if m['rating']]
                            if movies_with_rating:
                                top_rated = max(movies_with_rating, key=lambda x: x['rating'])
                                st.metric("Top Rated", top_rated['title'][:20] + "..." if len(top_rated['title']) > 20 else top_rated['title'])
                            else:
                                st.metric("Top Rated", "N/A")
                        
                    else:
                        st.warning(f"No movies found for the {selected_genre} genre.")
                except Exception as e:
                    st.error(f"Error getting recommendations: {e}")
            else:
                st.error("Please select a genre.")
        
        # Genre information
        st.markdown("---")
        st.subheader("ℹ️ About Genre Recommendations")
        
        st.markdown("""
        Our recommendation system works by:
        
        1. **Genre Selection**: Choose your preferred movie genre
        2. **Random Selection**: We randomly select movies from that genre
        3. **Personalized Results**: Get a fresh set of recommendations each time
        
        This simple approach ensures you discover new movies within your favorite genres!
        """)
        
        # Available genres display
        st.subheader("🎭 Available Genres")
        
        genre_cols = st.columns(3)
        for i, genre in enumerate(genres):
            with genre_cols[i % 3]:
                genre_emoji = get_genre_emoji(genre)
                st.markdown(f"**{genre_emoji} {genre}**")
                
                # Count movies in this genre
                try:
                    with st.spinner(f"Counting {genre} movies..."):
                        genre_movies = movie_api.get_movies_by_genre(genre, 8)  # Get all movies in genre
                        st.markdown(f"*{len(genre_movies)} movies available*")
                except Exception as e:
                    st.markdown(f"*Error counting movies: {e}*")
    
    except Exception as e:
        st.error(f"Unexpected error in genre recommendations page: {e}")
        st.write("Please check the console for more details.")
