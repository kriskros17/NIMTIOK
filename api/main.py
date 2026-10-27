
import csv
from fastapi import FastAPI

app = FastAPI()


class Movie:
    def __init__(self, movie_id: int, title: str, genres: list):
        self.movie_id = movie_id
        self.title = title
        self.genres = genres

class Link:
    def __init__(self, movie_id: int, imdb_id: str, tmdb_id: str):
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id

class Rating:
    def __init__(self, user_id: int, movie_id: int, rating: float, timestamp: int):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.timestamp = timestamp

class Tag:
    def __init__(self, user_id: int, movie_id: int, tag: str, timestamp: int):
        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = tag
        self.timestamp = timestamp

def read_rows(filename: str):
    rows = []
    with open(filename, encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return list(reader)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/links")
def get_links():
    links = [Link(movie_id=int(row[0]), imdb_id=row[1], tmdb_id=row[2]) for row in read_rows("database/links.csv")]
    return [link.__dict__ for link in links]

@app.get("/ratings")
def get_ratings():
    ratings = [Rating(user_id=int(row[0]), movie_id=int(row[1]), rating=float(row[2]), timestamp=int(row[3])) for row in read_rows("database/ratings.csv")]
    return [rating.__dict__ for rating in ratings]

@app.get("/movies")
def get_movies():
    movies = [Movie(movie_id=int(row[0]), title=row[1], genres=row[2].split("|")) for row in read_rows("database/movies.csv")]
    return [movie.__dict__ for movie in movies]


@app.get("/tags")
def get_tags():
    tags = [Tag(user_id=int(row[0]), movie_id=int(row[1]), tag=row[2], timestamp=int(row[3])) for row in read_rows("database/tags.csv")]
    return [tag.__dict__ for tag in tags]