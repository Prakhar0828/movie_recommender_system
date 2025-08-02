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
    st.title("🎯 Genre Recommendations")
    st.markdown("Select a genre to get personalized movie recommendations!")
    
    # Get available genres
    genres = movie_api.get_all_genres()
    
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
            # Get movies by genre
            recommended_movies = movie_api.get_movies_by_genre(selected_genre, limit)
            
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
                    avg_rating = sum(m['rating'] for m in recommended_movies if m['rating']) / len([m for m in recommended_movies if m['rating']])
                    st.metric("Average Rating", f"{avg_rating:.1f}/10")
                
                with col2:
                    year_range = f"{min(m['year'] for m in recommended_movies if m['year'])} - {max(m['year'] for m in recommended_movies if m['year'])}"
                    st.metric("Year Range", year_range)
                
                with col3:
                    top_rated = max(recommended_movies, key=lambda x: x['rating'] if x['rating'] else 0)
                    st.metric("Top Rated", top_rated['title'][:20] + "..." if len(top_rated['title']) > 20 else top_rated['title'])
                
            else:
                st.warning(f"No movies found for the {selected_genre} genre.")
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
            genre_movies = movie_api.get_movies_by_genre(genre, 1000)  # Get all movies in genre
            st.markdown(f"*{len(genre_movies)} movies available*")
