"""
Reusable movie card component for the movie recommendation frontend.
"""
import streamlit as st
import sys
import os
from typing import Dict, Any

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.helpers import format_cast_display, get_genre_emoji, get_genre_colors


def display_movie_card(movie: Dict[str, Any], show_details: bool = False) -> None:
    """
    Display a movie card with basic or detailed information.
    
    Args:
        movie: Movie data dictionary
        show_details: Whether to show detailed information
    """
    # Get genre styling
    genre_colors = get_genre_colors()
    genre = movie.get('genre', 'Unknown')
    genre_color = genre_colors.get(genre, '#808080')
    genre_emoji = get_genre_emoji(genre)
    
    # Create card container
    with st.container():
        # Card header with title and rating
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {movie.get('title', 'Unknown Title')}")
        
        with col2:
            rating = movie.get('rating')
            if rating:
                st.markdown(f"⭐ **{rating}/10**")
            else:
                st.markdown("⭐ **N/A**")
        
        # Genre badge
        st.markdown(
            f'<div style="background-color: {genre_color}; padding: 5px 10px; border-radius: 15px; display: inline-block; margin: 5px 0;">'
            f'{genre_emoji} {genre}</div>',
            unsafe_allow_html=True
        )
        
        # Basic info row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            year = movie.get('year')
            if year:
                st.markdown(f"**Year:** {year}")
            else:
                st.markdown("**Year:** N/A")
        
        with col2:
            director = movie.get('director')
            if director:
                st.markdown(f"**Director:** {director}")
            else:
                st.markdown("**Director:** N/A")
        
        with col3:
            movie_id = movie.get('id')
            if movie_id:
                st.markdown(f"**ID:** {movie_id}")
        
        # Show detailed information if requested
        if show_details:
            st.markdown("---")
            
            # Cast information
            cast = movie.get('cast', [])
            if cast:
                cast_display = format_cast_display(cast)
                st.markdown(f"**Cast:** {cast_display}")
            
            # Plot summary
            plot = movie.get('plot')
            if plot:
                st.markdown("**Plot:**")
                st.markdown(f"*{plot}*")
        
        st.markdown("---")


def display_movie_grid(movies: list, columns: int = 3, show_details: bool = False) -> None:
    """
    Display movies in a responsive grid layout.
    
    Args:
        movies: List of movie dictionaries
        columns: Number of columns in the grid
        show_details: Whether to show detailed information
    """
    if not movies:
        st.warning("No movies found.")
        return
    
    # Create grid layout
    for i in range(0, len(movies), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            if i + j < len(movies):
                with col:
                    display_movie_card(movies[i + j], show_details)


def display_movie_details(movie: Dict[str, Any]) -> None:
    """
    Display detailed movie information in a full-page format.
    
    Args:
        movie: Movie data dictionary
    """
    if not movie:
        st.error("Movie not found.")
        return
    
    # Header with title and rating
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.title(f"🎬 {movie.get('title', 'Unknown Title')}")
    
    with col2:
        rating = movie.get('rating')
        if rating:
            st.metric("Rating", f"{rating}/10")
        else:
            st.metric("Rating", "N/A")
    
    # Genre badge
    genre_colors = get_genre_colors()
    genre = movie.get('genre', 'Unknown')
    genre_color = genre_colors.get(genre, '#808080')
    genre_emoji = get_genre_emoji(genre)
    
    st.markdown(
        f'<div style="background-color: {genre_color}; padding: 10px 20px; border-radius: 20px; display: inline-block; margin: 10px 0;">'
        f'{genre_emoji} {genre}</div>',
        unsafe_allow_html=True
    )
    
    # Movie information in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Movie Information")
        year = movie.get('year')
        if year:
            st.markdown(f"**Release Year:** {year}")
        
        director = movie.get('director')
        if director:
            st.markdown(f"**Director:** {director}")
        
        movie_id = movie.get('id')
        if movie_id:
            st.markdown(f"**Movie ID:** {movie_id}")
    
    with col2:
        st.markdown("### 👥 Cast Information")
        cast = movie.get('cast', [])
        if cast:
            if isinstance(cast, list):
                for actor in cast:
                    st.markdown(f"• {actor}")
            else:
                st.markdown(f"• {cast}")
        else:
            st.markdown("Cast information not available")
    
    # Plot summary
    st.markdown("### 📖 Plot Summary")
    plot = movie.get('plot')
    if plot:
        st.markdown(f"*{plot}*")
    else:
        st.markdown("*Plot summary not available*")
    
    # Back button
    if st.button("← Back to Movies"):
        st.rerun()
