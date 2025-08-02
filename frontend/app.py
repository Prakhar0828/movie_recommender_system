"""
Main Streamlit application for the movie recommendation system.
"""
import streamlit as st
import sys
import os

# Add the frontend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages import home, genre_recommendations, movie_details
from components.api_client import movie_api


def main():
    """
    Main application function with navigation and page routing.
    """
    # Page configuration
    st.set_page_config(
        page_title="Movie Recommendation System",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .status-indicator {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
        text-align: center;
        margin: 5px 0;
    }
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown('<p class="sidebar-header">🎬 Movie Recommender</p>', unsafe_allow_html=True)
        
        # Backend connection status
        if movie_api.test_connection():
            st.markdown(
                '<div class="status-indicator status-connected">🟢 Backend Connected</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                '<div class="status-indicator status-disconnected">🔴 Backend Disconnected</div>',
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("🎯 Genre Recommendations", use_container_width=True):
            st.session_state.page = 'genre_recommendations'
            st.rerun()
        
        if st.button("🎬 Movie Details", use_container_width=True):
            st.session_state.page = 'movie_details'
            st.rerun()
        
        st.markdown("---")
        
        # App information
        st.markdown("### ℹ️ About")
        st.markdown("""
        A simple movie recommendation system that helps you discover new movies based on your preferred genres.
        
        **Features:**
        - Browse all movies
        - Get genre-based recommendations
        - Search and filter movies
        - View detailed movie information
        """)
        
        st.markdown("---")
        
        # Backend information
        st.markdown("### 🔗 Backend API")
        st.markdown(f"""
        **URL:** {movie_api.base_url}
        
        **Status:** {'🟢 Connected' if movie_api.test_connection() else '🔴 Disconnected'}
        
        **Docs:** [API Documentation]({movie_api.base_url}/docs)
        """)
        
        st.markdown("---")
        
        # Footer
        st.markdown("**Version:** 1.0.0")
        st.markdown("**Built with:** Streamlit + FastAPI")
    
    # Main content area
    if st.session_state.page == 'home':
        home.show_home_page()
    elif st.session_state.page == 'genre_recommendations':
        try:
            st.write("Debug: Loading genre recommendations page...")
            genre_recommendations.show_genre_recommendations()
        except Exception as e:
            st.error(f"Error loading genre recommendations page: {e}")
            st.write("Full error details:", e)
    elif st.session_state.page == 'movie_details':
        movie_details.show_movie_details()
    else:
        # Default to home page
        st.session_state.page = 'home'
        home.show_home_page()


if __name__ == "__main__":
    main()
