import csv
import os

from fastapi import FastAPI, HTTPException

from models import Link, Movie, Rating, Tag

app = FastAPI()

DB_DIR = "database"  # testy podmieniają to na folder tymczasowy

# plik -> (model, nagłówek CSV)
TABLES = {
    "movies.csv": (Movie, ["movieId", "title", "genres"]),
    "links.csv": (Link, ["movieId", "imdbId", "tmdbId"]),
    "ratings.csv": (Rating, ["userId", "movieId", "rating", "timestamp"]),
    "tags.csv": (Tag, ["userId", "movieId", "tag", "timestamp"]),
}


# ---------- CSV <-> lista obiektów ----------

def load(file):
    model, _ = TABLES[file]
    with open(os.path.join(DB_DIR, file), encoding="utf-8") as f:
        rows = list(csv.reader(f))[1:]  # bez nagłówka
    items = []
    for row in rows:
        data = dict(zip(model.model_fields, row))  # kolumny CSV są w tej samej kolejności co pola modelu
        if model is Movie:
            data["genres"] = data["genres"].split("|")
        items.append(model(**data))  # Pydantic sam zamieni "1" -> 1, "4.0" -> 4.0
    return items


def save(file, items):
    _, header = TABLES[file]
    with open(os.path.join(DB_DIR, file), "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in items:
            writer.writerow(["|".join(v) if isinstance(v, list) else v for v in item.model_dump().values()])


# ---------- wspólna logika CRUD ----------

def find(items, key):
    """Zwraca indeks elementu pasującego do key (np. {"movie_id": 1}) albo None."""
    for i, item in enumerate(items):
        if all(getattr(item, k) == v for k, v in key.items()):
            return i
    return None


def find_or_404(items, key):
    i = find(items, key)
    if i is None:
        raise HTTPException(status_code=404, detail="Not found")
    return i


def get_one(file, key):
    items = load(file)
    return items[find_or_404(items, key)]


def create(file, item, key_fields):
    items = load(file)
    key = {f: getattr(item, f) for f in key_fields}
    if find(items, key) is not None:
        raise HTTPException(status_code=409, detail="Already exists")
    items.append(item)
    save(file, items)
    return item


def update(file, key, item):
    items = load(file)
    items[find_or_404(items, key)] = item
    save(file, items)
    return item


def delete(file, key):
    items = load(file)
    items.pop(find_or_404(items, key))
    save(file, items)
    return {"deleted": key}


# ---------- endpointy ----------

@app.get("/")
def read_root():
    return {"Hello": "World"}


# MOVIES (klucz: movie_id)
@app.get("/movies")
def get_movies():
    return load("movies.csv")

@app.get("/movies/{movie_id}")
def get_movie(movie_id: int):
    return get_one("movies.csv", {"movie_id": movie_id})

@app.post("/movies", status_code=201)
def create_movie(movie: Movie):
    return create("movies.csv", movie, ["movie_id"])

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: Movie):
    return update("movies.csv", {"movie_id": movie_id}, movie)

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    return delete("movies.csv", {"movie_id": movie_id})


# LINKS (klucz: movie_id)
@app.get("/links")
def get_links():
    return load("links.csv")

@app.get("/links/{movie_id}")
def get_link(movie_id: int):
    return get_one("links.csv", {"movie_id": movie_id})

@app.post("/links", status_code=201)
def create_link(link: Link):
    return create("links.csv", link, ["movie_id"])

@app.put("/links/{movie_id}")
def update_link(movie_id: int, link: Link):
    return update("links.csv", {"movie_id": movie_id}, link)

@app.delete("/links/{movie_id}")
def delete_link(movie_id: int):
    return delete("links.csv", {"movie_id": movie_id})


# RATINGS (klucz: user_id + movie_id)
@app.get("/ratings")
def get_ratings():
    return load("ratings.csv")

@app.get("/ratings/{user_id}/{movie_id}")
def get_rating(user_id: int, movie_id: int):
    return get_one("ratings.csv", {"user_id": user_id, "movie_id": movie_id})

@app.post("/ratings", status_code=201)
def create_rating(rating: Rating):
    return create("ratings.csv", rating, ["user_id", "movie_id"])

@app.put("/ratings/{user_id}/{movie_id}")
def update_rating(user_id: int, movie_id: int, rating: Rating):
    return update("ratings.csv", {"user_id": user_id, "movie_id": movie_id}, rating)

@app.delete("/ratings/{user_id}/{movie_id}")
def delete_rating(user_id: int, movie_id: int):
    return delete("ratings.csv", {"user_id": user_id, "movie_id": movie_id})


# TAGS (klucz: user_id + movie_id + tag)
@app.get("/tags")
def get_tags():
    return load("tags.csv")

@app.get("/tags/{user_id}/{movie_id}/{tag}")
def get_tag(user_id: int, movie_id: int, tag: str):
    return get_one("tags.csv", {"user_id": user_id, "movie_id": movie_id, "tag": tag})

@app.post("/tags", status_code=201)
def create_tag(new_tag: Tag):
    return create("tags.csv", new_tag, ["user_id", "movie_id", "tag"])

@app.put("/tags/{user_id}/{movie_id}/{tag}")
def update_tag(user_id: int, movie_id: int, tag: str, new_tag: Tag):
    return update("tags.csv", {"user_id": user_id, "movie_id": movie_id, "tag": tag}, new_tag)

@app.delete("/tags/{user_id}/{movie_id}/{tag}")
def delete_tag(user_id: int, movie_id: int, tag: str):
    return delete("tags.csv", {"user_id": user_id, "movie_id": movie_id, "tag": tag})