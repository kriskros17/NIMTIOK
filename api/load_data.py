# load_data.py - ten plik uruchamiasz RAZ.
# Czyta pliki CSV i przepisuje wszystko do bazy SQLite (plik database/movies.db).

import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Movie, Link, Rating, Tag

# engine = połączenie z bazą. Jeśli pliku movies.db nie ma, zostanie utworzony.
engine = create_engine("sqlite:///database/movies.db")

# Usuwamy stare tabele (jeśli były) i tworzymy nowe, puste.
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# session = "rozmowa z bazą". W niej dodajemy wiersze, a na końcu zatwierdzamy.
with Session(engine) as session:

    # --- movies ---
    with open("database/movies.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # pomijamy pierwszy wiersz z nagłówkami
        for row in reader:
            # row to lista, np. ["1", "Toy Story (1995)", "Adventure|Animation"]
            movie = Movie(movie_id=int(row[0]), title=row[1], genres=row[2])
            session.add(movie)

    # --- links ---
    with open("database/links.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            link = Link(movie_id=int(row[0]), imdb_id=row[1], tmdb_id=row[2])
            session.add(link)

    # --- ratings ---
    with open("database/ratings.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            rating = Rating(user_id=int(row[0]), movie_id=int(row[1]), rating=float(row[2]), timestamp=int(row[3]))
            session.add(rating)

    # --- tags ---
    with open("database/tags.csv", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tag = Tag(user_id=int(row[0]), movie_id=int(row[1]), tag=row[2], timestamp=int(row[3]))
            session.add(tag)

    # Dopiero tutaj wszystko naprawdę zapisuje się w bazie.
    session.commit()

print("Gotowe - dane są w bazie")
