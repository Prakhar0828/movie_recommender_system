"""
Movie details page for the movie recommendation frontend.
Shows detailed information about a specific movie.
"""
import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.api_client import movie_api
from components.movie_card import display_movie_details
from utils.helpers import format_movie_data


def show_movie_details():
    """
    Display the movie details page.
    """
    st.title("🎬 Movie Details")
    st.markdown("View detailed information about a specific movie.")
    
    # Movie selection
    movies = movie_api.get_all_movies()
    movie_titles = [f"{movie['title']} ({movie['year']})" for movie in movies]
    
    selected_movie_title = st.selectbox(
        "Select a movie to view details",
        movie_titles,
        index=0,
        help="Choose a movie from the dropdown to see its details"
    )
    
    # Find the selected movie
    selected_movie = None
    for movie in movies:
        if f"{movie['title']} ({movie['year']})" == selected_movie_title:
            selected_movie = movie
            break
    
    if selected_movie:
        # Format movie data
        formatted_movie = format_movie_data(selected_movie)
        
        # Display movie details
        display_movie_details(formatted_movie)
        
        # Similar movies section
        st.markdown("---")
        st.subheader("🎭 Similar Movies")
        
        # Get movies from the same genre
        same_genre_movies = movie_api.get_movies_by_genre(selected_movie['genre'], 4)
        same_genre_movies = [m for m in same_genre_movies if m['id'] != selected_movie['id']]
        
        if same_genre_movies:
            st.markdown(f"**Other {selected_movie['genre']} movies you might like:**")
            
            # Display similar movies in a horizontal layout
            cols = st.columns(len(same_genre_movies))
            for i, movie in enumerate(same_genre_movies):
                with cols[i]:
                    st.markdown(f"**{movie['title']}**")
                    st.markdown(f"*{movie['year']}*")
                    if movie['rating']:
                        st.markdown(f"⭐ {movie['rating']}/10")
                    st.markdown(f"🎬 {movie['director']}")
        else:
            st.info(f"No other {selected_movie['genre']} movies available.")
        
        # Movie recommendations section
        st.markdown("---")
        st.subheader("💡 Get More Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Get Genre Recommendations"):
                st.session_state.page = "genre_recommendations"
                st.rerun()
        
        with col2:
            if st.button("🏠 Back to All Movies"):
                st.session_state.page = "home"
                st.rerun()
    
    else:
        st.error("Movie not found. Please select a valid movie from the dropdown.")
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Back to All Movies"):
                st.session_state.page = "home"
                st.rerun()
        
        with col2:
            if st.button("🎯 Get Genre Recommendations"):
                st.session_state.page = "genre_recommendations"
                st.rerun()
