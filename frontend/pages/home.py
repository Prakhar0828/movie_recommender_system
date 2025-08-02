"""
Home page for the movie recommendation frontend.
Displays all movies with search and filtering options.
"""
import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.api_client import movie_api
from components.movie_card import display_movie_grid
from utils.helpers import format_movie_data, validate_year_range, validate_rating


def show_home_page():
    """
    Display the home page with all movies and filtering options.
    """
    st.title("🎬 Movie Recommendation System")
    st.markdown("Discover and explore movies from our collection!")
    
    # Get all movies
    movies = movie_api.get_all_movies()
    
    # Sidebar for filtering options
    with st.sidebar:
        st.header("🔍 Filter Options")
        
        # Search by title
        search_term = st.text_input("Search by title", placeholder="Enter movie title...")
        
        # Filter by genre
        genres = movie_api.get_all_genres()
        selected_genre = st.selectbox("Filter by genre", ["All Genres"] + genres)
        
        # Filter by year range
        st.subheader("Year Range")
        col1, col2 = st.columns(2)
        with col1:
            start_year = st.number_input("From", min_value=1888, max_value=2030, value=1900)
        with col2:
            end_year = st.number_input("To", min_value=1888, max_value=2030, value=2030)
        
        # Filter by rating
        st.subheader("Minimum Rating")
        min_rating = st.slider("Rating", min_value=0.0, max_value=10.0, value=0.0, step=0.5)
        
        # Apply filters button
        apply_filters = st.button("Apply Filters", type="primary")
        
        # Clear filters button
        if st.button("Clear Filters"):
            st.rerun()
    
    # Apply filters
    filtered_movies = movies.copy()
    
    if apply_filters or search_term or selected_genre != "All Genres" or min_rating > 0.0:
        # Search by title
        if search_term:
            filtered_movies = [m for m in filtered_movies if search_term.lower() in m['title'].lower()]
        
        # Filter by genre
        if selected_genre != "All Genres":
            filtered_movies = [m for m in filtered_movies if m['genre'] == selected_genre]
        
        # Filter by year range
        if validate_year_range(start_year, end_year):
            filtered_movies = [m for m in filtered_movies if m['year'] and start_year <= m['year'] <= end_year]
        
        # Filter by rating
        if min_rating > 0.0:
            filtered_movies = [m for m in filtered_movies if m['rating'] and m['rating'] >= min_rating]
    
    # Display results
    st.subheader(f"📽️ Movies ({len(filtered_movies)} found)")
    
    if not filtered_movies:
        st.warning("No movies found matching your criteria. Try adjusting your filters.")
        return
    
    # Format movies for display
    formatted_movies = [format_movie_data(movie) for movie in filtered_movies]
    
    # Display options
    col1, col2 = st.columns([1, 4])
    with col1:
        show_details = st.checkbox("Show Details", value=False)
    with col2:
        columns = st.selectbox("Columns", [2, 3, 4], index=1)
    
    # Display movies in grid
    display_movie_grid(formatted_movies, columns=columns, show_details=show_details)
    
    # Movie statistics
    if filtered_movies:
        st.markdown("---")
        st.subheader("📊 Movie Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = sum(m['rating'] for m in filtered_movies if m['rating']) / len([m for m in filtered_movies if m['rating']])
            st.metric("Average Rating", f"{avg_rating:.1f}/10")
        
        with col2:
            year_range = f"{min(m['year'] for m in filtered_movies if m['year'])} - {max(m['year'] for m in filtered_movies if m['year'])}"
            st.metric("Year Range", year_range)
        
        with col3:
            genre_counts = {}
            for movie in filtered_movies:
                genre = movie['genre']
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
            most_common_genre = max(genre_counts.items(), key=lambda x: x[1])[0]
            st.metric("Most Common Genre", most_common_genre)
        
        with col4:
            top_rated = max(filtered_movies, key=lambda x: x['rating'] if x['rating'] else 0)
            st.metric("Top Rated", top_rated['title'][:20] + "..." if len(top_rated['title']) > 20 else top_rated['title'])
