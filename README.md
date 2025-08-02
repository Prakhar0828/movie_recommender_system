# Movie Recommendation System

A simple movie recommendation system built with FastAPI (backend) and Streamlit (frontend). The system provides movie recommendations based on genres using a SQLite database.

## Features

- **Movie Browsing**: View all movies in the database
- **Genre-based Recommendations**: Get random movie suggestions for specific genres
- **Movie Details**: View detailed information about individual movies
- **Search Functionality**: Search movies by title
- **Year and Rating Filtering**: Filter movies by year range or minimum rating
- **RESTful API**: Clean API endpoints for all operations

## Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight database for data storage
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **Streamlit**: Rapid web app development framework
- **Requests**: HTTP library for API communication

## Project Structure

```
movie_recommender_system/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── models/                 # Pydantic models
│   │   ├── database/               # Database configuration
│   │   ├── routers/                # API endpoints
│   │   ├── services/               # Business logic
│   │   └── utils/                  # Utilities
│   ├── requirements.txt
│   └── init_db.py                  # Database initialization
├── frontend/
│   ├── app.py                      # Main Streamlit app
│   ├── pages/                      # Streamlit pages
│   ├── components/                 # Reusable components
│   └── requirements.txt
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd movie_recommender_system/backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   python init_db.py
   ```

4. **Start the FastAPI server:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd movie_recommender_system/frontend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

The frontend will be available at `http://localhost:8501`

## API Documentation

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### Movies

- `GET /movies/` - Get all movies
- `GET /movies/{movie_id}` - Get movie by ID
- `GET /movies/genre/{genre}` - Get random movies by genre
- `GET /movies/search/?query={search_term}` - Search movies by title
- `GET /movies/year/{start_year}/{end_year}` - Get movies by year range
- `GET /movies/rating/{min_rating}` - Get movies by minimum rating

#### Genres

- `GET /genres/` - Get all available genres

### Interactive API Documentation

Once the backend is running, you can access:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Sample API Requests

### Get All Movies
```bash
curl http://localhost:8000/movies/
```

### Get Movies by Genre
```bash
curl http://localhost:8000/movies/genre/Action?limit=5
```

### Search Movies
```bash
curl "http://localhost:8000/movies/search/?query=dark"
```

### Get All Genres
```bash
curl http://localhost:8000/genres/
```

## Database Schema

### Movies Table
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| title | VARCHAR(255) | Movie title |
| year | INTEGER | Release year |
| genre | VARCHAR(100) | Movie genre |
| rating | FLOAT | Rating score (0-10) |
| director | VARCHAR(255) | Movie director |
| cast | TEXT | Cast members (JSON string) |
| plot | TEXT | Movie plot summary |

## Sample Data

The system comes pre-loaded with 24 movies across 6 genres:
- **Action**: The Dark Knight, Mad Max: Fury Road, John Wick, Mission: Impossible - Fallout
- **Comedy**: The Grand Budapest Hotel, Superbad, Bridesmaids, The Hangover
- **Drama**: The Shawshank Redemption, Forrest Gump, The Green Mile, Schindler's List
- **Horror**: The Shining, A Quiet Place, Get Out, Hereditary
- **Sci-Fi**: Inception, Interstellar, Blade Runner 2049, Arrival
- **Thriller**: Gone Girl, The Silence of the Lambs, Se7en, Zodiac

## Development

### Adding New Movies

To add new movies to the database, modify the `SAMPLE_MOVIES` list in `backend/app/utils/data_seeder.py` and re-run the initialization script.

### Extending the API

The modular architecture makes it easy to add new endpoints:
1. Add new methods to `MovieService` in `backend/app/services/movie_service.py`
2. Create new endpoints in `backend/app/routers/movies.py`
3. Update Pydantic models in `backend/app/models/movie.py` if needed

### Error Handling

The API includes comprehensive error handling:
- **404**: Resource not found
- **422**: Validation errors
- **500**: Internal server errors

All errors return consistent JSON responses with error details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
