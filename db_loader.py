import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Load scraped data
df = pd.read_csv("src/data/books_with_descriptions.csv")

# SQLAlchemy setup
Base = declarative_base()

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    books = relationship("Book", back_populates="genre")

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    price = Column(Float)
    availability = Column(String)
    rating = Column(Integer)
    description = Column(Text)
    genre_id = Column(Integer, ForeignKey('genres.id'))
    genre = relationship("Genre", back_populates="books")

# Create SQLite engine
engine = create_engine("sqlite:///src/data/books.db")
Base.metadata.drop_all(engine)  # Optional: drop existing tables
Base.metadata.create_all(engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Insert genres and books
genre_map = {}

for _, row in df.iterrows():
    genre_name = row['genre']

    # Get or create genre
    if genre_name not in genre_map:
        genre_obj = Genre(name=genre_name)
        session.add(genre_obj)
        session.flush()  # Get id without committing
        genre_map[genre_name] = genre_obj.id

    # Add book
    book = Book(
        title=row['title'],
        price=row['price'],
        availability=row['availability'],
        rating=row['rating'],
        description=row['description'],
        genre_id=genre_map[genre_name]
    )
    session.add(book)

session.commit()
print("✅ Database created at src/data/books.db")
