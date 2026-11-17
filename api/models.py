from pydantic import BaseModel


class Movie(BaseModel):
    movie_id: int
    title: str
    genres: list[str]


class Link(BaseModel):
    movie_id: int
    imdb_id: str
    tmdb_id: str


class Rating(BaseModel):
    user_id: int
    movie_id: int
    rating: float
    timestamp: int


class Tag(BaseModel):
    user_id: int
    movie_id: int
    tag: str
    timestamp: int