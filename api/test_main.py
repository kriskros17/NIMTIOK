import csv

import pytest
from fastapi.testclient import TestClient

import main

# ---------------------------------------------------------------------
# FIXTURY – małe, przewidywalne dane testowe
# ---------------------------------------------------------------------

MOVIES = [
    ["1", "Toy Story (1995)", "Adventure|Animation|Children|Comedy|Fantasy"],
    ["2", "Jumanji (1995)", "Adventure|Children|Fantasy"],
    ["3", "Grumpier Old Men (1995)", "Comedy|Romance"],
]
LINKS = [
    ["1", "0114709", "862"],
    ["2", "0113497", "8844"],
]
RATINGS = [
    ["1", "1", "4.0", "964982703"],
    ["1", "3", "4.0", "964981247"],
    ["2", "1", "3.5", "964982224"],
]
TAGS = [
    ["2", "60756", "funny", "1445714994"],
    ["2", "60756", "Highly quotable", "1445714996"],
]


def write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Tworzy tymczasową 'bazę' (4 pliki CSV) i podpina ją pod aplikację.
    Każdy test dostaje świeżą kopię, więc testy nie wpływają na siebie."""
    write_csv(tmp_path / "movies.csv", main.TABLES["movies.csv"][1], MOVIES)
    write_csv(tmp_path / "links.csv", main.TABLES["links.csv"][1], LINKS)
    write_csv(tmp_path / "ratings.csv", main.TABLES["ratings.csv"][1], RATINGS)
    write_csv(tmp_path / "tags.csv", main.TABLES["tags.csv"][1], TAGS)
    monkeypatch.setattr(main, "DB_DIR", str(tmp_path))
    return TestClient(main.app)


# =====================================================================
# MOVIES
# =====================================================================

def test_get_movies_returns_all(client):
    r = client.get("/movies")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == len(MOVIES)
    assert data[0]["title"] == "Toy Story (1995)"
    assert data[0]["genres"] == ["Adventure", "Animation", "Children", "Comedy", "Fantasy"]


def test_get_movie_by_id(client):
    r = client.get("/movies/2")
    assert r.status_code == 200
    assert r.json()["movie_id"] == 2
    assert r.json()["title"] == "Jumanji (1995)"


def test_get_movie_not_found(client):
    r = client.get("/movies/999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Not found"


def test_create_movie(client):
    new = {"movie_id": 10, "title": "Matrix (1999)", "genres": ["Action", "Sci-Fi"]}
    r = client.post("/movies", json=new)
    assert r.status_code == 201
    assert r.json() == new
    # czy jest w bazie?
    assert client.get("/movies/10").json() == new
    assert len(client.get("/movies").json()) == len(MOVIES) + 1


def test_create_movie_duplicate(client):
    r = client.post("/movies", json={"movie_id": 1, "title": "X", "genres": []})
    assert r.status_code == 409
    assert len(client.get("/movies").json()) == len(MOVIES)


def test_update_movie(client):
    r = client.put("/movies/1", json={"movie_id": 1, "title": "Toy Story 2", "genres": ["Animation"]})
    assert r.status_code == 200
    stored = client.get("/movies/1").json()
    assert stored["title"] == "Toy Story 2"
    assert stored["genres"] == ["Animation"]
    assert len(client.get("/movies").json()) == len(MOVIES)


def test_update_movie_not_found(client):
    r = client.put("/movies/999", json={"movie_id": 999, "title": "X", "genres": []})
    assert r.status_code == 404


def test_delete_movie(client):
    r = client.delete("/movies/3")
    assert r.status_code == 200
    assert client.get("/movies/3").status_code == 404
    assert len(client.get("/movies").json()) == len(MOVIES) - 1


def test_delete_movie_not_found(client):
    assert client.delete("/movies/999").status_code == 404
    assert len(client.get("/movies").json()) == len(MOVIES)


# =====================================================================
# LINKS
# =====================================================================

def test_get_links_returns_all(client):
    r = client.get("/links")
    assert r.status_code == 200
    assert len(r.json()) == len(LINKS)


def test_get_link_by_id(client):
    r = client.get("/links/1")
    assert r.status_code == 200
    assert r.json() == {"movie_id": 1, "imdb_id": "0114709", "tmdb_id": "862"}


def test_get_link_not_found(client):
    assert client.get("/links/999").status_code == 404


def test_create_link(client):
    new = {"movie_id": 3, "imdb_id": "0113228", "tmdb_id": "15602"}
    r = client.post("/links", json=new)
    assert r.status_code == 201
    assert client.get("/links/3").json() == new
    assert len(client.get("/links").json()) == len(LINKS) + 1


def test_update_link(client):
    r = client.put("/links/2", json={"movie_id": 2, "imdb_id": "0000001", "tmdb_id": "1"})
    assert r.status_code == 200
    stored = client.get("/links/2").json()
    assert stored["imdb_id"] == "0000001"
    assert stored["tmdb_id"] == "1"


def test_delete_link(client):
    assert client.delete("/links/1").status_code == 200
    assert client.get("/links/1").status_code == 404
    assert len(client.get("/links").json()) == len(LINKS) - 1


# =====================================================================
# RATINGS
# =====================================================================

def test_get_ratings_returns_all(client):
    r = client.get("/ratings")
    assert r.status_code == 200
    assert len(r.json()) == len(RATINGS)
    assert r.json()[0]["rating"] == 4.0


def test_get_rating_by_id(client):
    r = client.get("/ratings/2/1")
    assert r.status_code == 200
    assert r.json()["user_id"] == 2
    assert r.json()["movie_id"] == 1
    assert r.json()["rating"] == 3.5


def test_get_rating_not_found(client):
    assert client.get("/ratings/1/2").status_code == 404


def test_create_rating(client):
    new = {"user_id": 5, "movie_id": 2, "rating": 5.0, "timestamp": 1700000000}
    r = client.post("/ratings", json=new)
    assert r.status_code == 201
    assert client.get("/ratings/5/2").json() == new
    assert len(client.get("/ratings").json()) == len(RATINGS) + 1


def test_create_rating_invalid_body(client):
    # brak pola "rating" -> walidacja Pydantic -> 422
    r = client.post("/ratings", json={"user_id": 5, "movie_id": 2, "timestamp": 1})
    assert r.status_code == 422
    assert len(client.get("/ratings").json()) == len(RATINGS)


def test_update_rating(client):
    r = client.put("/ratings/1/1", json={"user_id": 1, "movie_id": 1, "rating": 1.5, "timestamp": 1})
    assert r.status_code == 200
    stored = client.get("/ratings/1/1").json()
    assert stored["rating"] == 1.5
    assert stored["timestamp"] == 1


def test_delete_rating(client):
    assert client.delete("/ratings/1/3").status_code == 200
    assert client.get("/ratings/1/3").status_code == 404
    assert len(client.get("/ratings").json()) == len(RATINGS) - 1


# =====================================================================
# TAGS
# =====================================================================

def test_get_tags_returns_all(client):
    r = client.get("/tags")
    assert r.status_code == 200
    assert len(r.json()) == len(TAGS)


def test_get_tag_by_id(client):
    r = client.get("/tags/2/60756/funny")
    assert r.status_code == 200
    assert r.json()["tag"] == "funny"
    assert r.json()["timestamp"] == 1445714994


def test_get_tag_with_space_in_name(client):
    r = client.get("/tags/2/60756/Highly quotable")  # TestClient sam zakoduje spację
    assert r.status_code == 200
    assert r.json()["tag"] == "Highly quotable"


def test_get_tag_not_found(client):
    assert client.get("/tags/2/60756/boring").status_code == 404


def test_create_tag(client):
    new = {"user_id": 7, "movie_id": 1, "tag": "pixar", "timestamp": 1700000000}
    r = client.post("/tags", json=new)
    assert r.status_code == 201
    assert client.get("/tags/7/1/pixar").json() == new
    assert len(client.get("/tags").json()) == len(TAGS) + 1


def test_update_tag(client):
    body = {"user_id": 2, "movie_id": 60756, "tag": "very funny", "timestamp": 1}
    r = client.put("/tags/2/60756/funny", json=body)
    assert r.status_code == 200
    assert client.get("/tags/2/60756/funny").status_code == 404
    assert client.get("/tags/2/60756/very funny").json()["timestamp"] == 1
    assert len(client.get("/tags").json()) == len(TAGS)


def test_delete_tag(client):
    assert client.delete("/tags/2/60756/funny").status_code == 200
    assert client.get("/tags/2/60756/funny").status_code == 404
    # drugi tag tego samego usera/filmu nadal istnieje
    assert client.get("/tags/2/60756/Highly quotable").status_code == 200
    assert len(client.get("/tags").json()) == len(TAGS) - 1