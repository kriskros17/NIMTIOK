# main.py - nasze API. Teraz dane biorą się z bazy, a nie z plików CSV.

from fastapi import FastAPI
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Movie, Link, Rating, Tag

# połączenie z tą samą bazą, którą zapełnił load_data.py
engine = create_engine("sqlite:///database/movies.db")

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movies")
def get_movies():
    with Session(engine) as session:
        # "daj mi wszystkie filmy z bazy"
        movies = session.scalars(select(Movie)).all()

    result = []
    for movie in movies:
        result.append({
            "movie_id": movie.movie_id,
            "title": movie.title,
            "genres": movie.genres.split("|"),  # tekst zamieniamy z powrotem na listę
        })
    return result


@app.get("/links")
def get_links():
    with Session(engine) as session:
        links = session.scalars(select(Link)).all()

    result = []
    for link in links:
        result.append({
            "movie_id": link.movie_id,
            "imdb_id": link.imdb_id,
            "tmdb_id": link.tmdb_id,
        })
    return result


@app.get("/ratings")
def get_ratings():
    with Session(engine) as session:
        ratings = session.scalars(select(Rating)).all()

    result = []
    for rating in ratings:
        result.append({
            "user_id": rating.user_id,
            "movie_id": rating.movie_id,
            "rating": rating.rating,
            "timestamp": rating.timestamp,
        })
    return result


@app.get("/tags")
def get_tags():
    with Session(engine) as session:
        tags = session.scalars(select(Tag)).all()

    result = []
    for tag in tags:
        result.append({
            "user_id": tag.user_id,
            "movie_id": tag.movie_id,
            "tag": tag.tag,
            "timestamp": tag.timestamp,
        })
    return result
