# models.py - tutaj opisujemy, jak mają wyglądać tabele w bazie.
# Jedna klasa = jedna tabela. Jedna zmienna w klasie = jedna kolumna.

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Base to "wzór" dla wszystkich naszych tabel. Każda tabela po nim dziedziczy.
class Base(DeclarativeBase):
    pass


# Tabela movies (filmy)
class Movie(Base):
    __tablename__ = "movies"  # nazwa tabeli w bazie

    movie_id: Mapped[int] = mapped_column(primary_key=True)  # numer filmu, unikalny
    title: Mapped[str]  # tytuł (tekst)
    genres: Mapped[str]  # gatunki jako jeden tekst, np. "Adventure|Comedy"


# Tabela links (linki do IMDB i TMDB)
class Link(Base):
    __tablename__ = "links"

    movie_id: Mapped[int] = mapped_column(primary_key=True)
    imdb_id: Mapped[str]  # tekst, bo ma zera z przodu, np. "0114709"
    tmdb_id: Mapped[str]


# Tabela ratings (oceny)
class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)  # numer wiersza, baza nadaje go sama
    user_id: Mapped[int]
    movie_id: Mapped[int]
    rating: Mapped[float]  # ocena, np. 4.5
    timestamp: Mapped[int]


# Tabela tags (tagi)
class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)  # numer wiersza, baza nadaje go sama
    user_id: Mapped[int]
    movie_id: Mapped[int]
    tag: Mapped[str]
    timestamp: Mapped[int]
