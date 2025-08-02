"""
Data seeder utility for populating the database with sample movie data.
"""
import json
from sqlalchemy.orm import Session
from ..database.models import Movie


# Sample movie data for the MVP
SAMPLE_MOVIES = [
    # Action Movies
    {
        "title": "The Dark Knight",
        "year": 2008,
        "genre": "Action",
        "rating": 9.0,
        "director": "Christopher Nolan",
        "cast": json.dumps(["Christian Bale", "Heath Ledger", "Aaron Eckhart"]),
        "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice."
    },
    {
        "title": "Mad Max: Fury Road",
        "year": 2015,
        "genre": "Action",
        "rating": 8.1,
        "director": "George Miller",
        "cast": json.dumps(["Tom Hardy", "Charlize Theron", "Nicholas Hoult"]),
        "plot": "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max."
    },
    {
        "title": "John Wick",
        "year": 2014,
        "genre": "Action",
        "rating": 7.4,
        "director": "Chad Stahelski",
        "cast": json.dumps(["Keanu Reeves", "Michael Nyqvist", "Alfie Allen"]),
        "plot": "An ex-hitman comes out of retirement to track down the gangsters who killed his dog and stole his car."
    },
    {
        "title": "Mission: Impossible - Fallout",
        "year": 2018,
        "genre": "Action",
        "rating": 7.7,
        "director": "Christopher McQuarrie",
        "cast": json.dumps(["Tom Cruise", "Henry Cavill", "Ving Rhames"]),
        "plot": "Ethan Hunt and his IMF team, along with some familiar allies, race against time after a mission goes wrong."
    },
    
    # Comedy Movies
    {
        "title": "The Grand Budapest Hotel",
        "year": 2014,
        "genre": "Comedy",
        "rating": 8.1,
        "director": "Wes Anderson",
        "cast": json.dumps(["Ralph Fiennes", "Tony Revolori", "F. Murray Abraham"]),
        "plot": "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge."
    },
    {
        "title": "Superbad",
        "year": 2007,
        "genre": "Comedy",
        "rating": 7.6,
        "director": "Greg Mottola",
        "cast": json.dumps(["Jonah Hill", "Michael Cera", "Christopher Mintz-Plasse"]),
        "plot": "Two co-dependent high school seniors are forced to deal with separation anxiety after their plan to stage a booze-soaked party goes awry."
    },
    {
        "title": "Bridesmaids",
        "year": 2011,
        "genre": "Comedy",
        "rating": 6.8,
        "director": "Paul Feig",
        "cast": json.dumps(["Kristen Wiig", "Maya Rudolph", "Rose Byrne"]),
        "plot": "Competition between the maid of honor and a bridesmaid, over who is the bride's best friend, threatens to upend the life of an out-of-work pastry chef."
    },
    {
        "title": "The Hangover",
        "year": 2009,
        "genre": "Comedy",
        "rating": 7.7,
        "director": "Todd Phillips",
        "cast": json.dumps(["Bradley Cooper", "Ed Helms", "Zach Galifianakis"]),
        "plot": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding."
    },
    
    # Drama Movies
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "genre": "Drama",
        "rating": 9.3,
        "director": "Frank Darabont",
        "cast": json.dumps(["Tim Robbins", "Morgan Freeman", "Bob Gunton"]),
        "plot": "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency."
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "genre": "Drama",
        "rating": 8.8,
        "director": "Robert Zemeckis",
        "cast": json.dumps(["Tom Hanks", "Robin Wright", "Gary Sinise"]),
        "plot": "The presidencies of Kennedy and Johnson, the Vietnam War, the Watergate scandal and other historical events unfold from the perspective of an Alabama man with an IQ of 75."
    },
    {
        "title": "The Green Mile",
        "year": 1999,
        "genre": "Drama",
        "rating": 8.6,
        "director": "Frank Darabont",
        "cast": json.dumps(["Tom Hanks", "Michael Clarke Duncan", "David Morse"]),
        "plot": "The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder and rape, yet who has a mysterious gift."
    },
    {
        "title": "Schindler's List",
        "year": 1993,
        "genre": "Drama",
        "rating": 8.9,
        "director": "Steven Spielberg",
        "cast": json.dumps(["Liam Neeson", "Ralph Fiennes", "Ben Kingsley"]),
        "plot": "In German-occupied Poland during World War II, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution by the Nazis."
    },
    
    # Horror Movies
    {
        "title": "The Shining",
        "year": 1980,
        "genre": "Horror",
        "rating": 8.4,
        "director": "Stanley Kubrick",
        "cast": json.dumps(["Jack Nicholson", "Shelley Duvall", "Danny Lloyd"]),
        "plot": "A family heads to an isolated hotel for the winter where a sinister presence influences the father into violence, while his psychic son sees horrific forebodings from both past and future."
    },
    {
        "title": "A Quiet Place",
        "year": 2018,
        "genre": "Horror",
        "rating": 7.5,
        "director": "John Krasinski",
        "cast": json.dumps(["Emily Blunt", "John Krasinski", "Millicent Simmonds"]),
        "plot": "In a post-apocalyptic world, a family is forced to live in silence while hiding from monsters with ultra-sensitive hearing."
    },
    {
        "title": "Get Out",
        "year": 2017,
        "genre": "Horror",
        "rating": 7.7,
        "director": "Jordan Peele",
        "cast": json.dumps(["Daniel Kaluuya", "Allison Williams", "Bradley Whitford"]),
        "plot": "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point."
    },
    {
        "title": "Hereditary",
        "year": 2018,
        "genre": "Horror",
        "rating": 7.3,
        "director": "Ari Aster",
        "cast": json.dumps(["Toni Collette", "Milly Shapiro", "Gabriel Byrne"]),
        "plot": "A grieving family is haunted by tragic and disturbing occurrences."
    },
    
    # Sci-Fi Movies
    {
        "title": "Inception",
        "year": 2010,
        "genre": "Sci-Fi",
        "rating": 8.8,
        "director": "Christopher Nolan",
        "cast": json.dumps(["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"]),
        "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "title": "Interstellar",
        "year": 2014,
        "genre": "Sci-Fi",
        "rating": 8.6,
        "director": "Christopher Nolan",
        "cast": json.dumps(["Matthew McConaughey", "Anne Hathaway", "Jessica Chastain"]),
        "plot": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."
    },
    {
        "title": "Blade Runner 2049",
        "year": 2017,
        "genre": "Sci-Fi",
        "rating": 8.0,
        "director": "Denis Villeneuve",
        "cast": json.dumps(["Ryan Gosling", "Harrison Ford", "Ana de Armas"]),
        "plot": "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who's been missing for thirty years."
    },
    {
        "title": "Arrival",
        "year": 2016,
        "genre": "Sci-Fi",
        "rating": 7.9,
        "director": "Denis Villeneuve",
        "cast": json.dumps(["Amy Adams", "Jeremy Renner", "Forest Whitaker"]),
        "plot": "A linguist works with the military to communicate with alien lifeforms after twelve mysterious spacecraft appear around the world."
    },
    
    # Thriller Movies
    {
        "title": "Gone Girl",
        "year": 2014,
        "genre": "Thriller",
        "rating": 8.1,
        "director": "David Fincher",
        "cast": json.dumps(["Ben Affleck", "Rosamund Pike", "Neil Patrick Harris"]),
        "plot": "With his wife's disappearance having become the focus of an intense media circus, a man sees the spotlight turned on him when it's suspected that he may not be innocent."
    },
    {
        "title": "The Silence of the Lambs",
        "year": 1991,
        "genre": "Thriller",
        "rating": 8.6,
        "director": "Jonathan Demme",
        "cast": json.dumps(["Jodie Foster", "Anthony Hopkins", "Lawrence A. Bonney"]),
        "plot": "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer, a madman who skins his victims."
    },
    {
        "title": "Se7en",
        "year": 1995,
        "genre": "Thriller",
        "rating": 8.6,
        "director": "David Fincher",
        "cast": json.dumps(["Morgan Freeman", "Brad Pitt", "Kevin Spacey"]),
        "plot": "Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives."
    },
    {
        "title": "Zodiac",
        "year": 2007,
        "genre": "Thriller",
        "rating": 7.7,
        "director": "David Fincher",
        "cast": json.dumps(["Jake Gyllenhaal", "Robert Downey Jr.", "Mark Ruffalo"]),
        "plot": "Between 1968 and 1983, a San Francisco cartoonist becomes an amateur detective obsessed with tracking down the Zodiac Killer, an unidentified individual who terrorizes Northern California with a killing spree."
    }
]


def seed_database(database_session: Session) -> None:
    """
    Seed the database with sample movie data.
    
    Args:
        database_session: SQLAlchemy database session
    """
    try:
        # Check if database is already seeded
        existing_movies = database_session.query(Movie).count()
        if existing_movies > 0:
            print(f"Database already contains {existing_movies} movies. Skipping seeding.")
            return
        
        # Add sample movies to database
        for movie_data in SAMPLE_MOVIES:
            movie = Movie(**movie_data)
            database_session.add(movie)
        
        # Commit the changes
        database_session.commit()
        print(f"Successfully seeded database with {len(SAMPLE_MOVIES)} movies!")
        
    except Exception as e:
        database_session.rollback()
        print(f"Error seeding database: {e}")
        raise
