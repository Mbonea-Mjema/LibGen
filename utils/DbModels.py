from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from dataclasses import dataclass
from dataclasses import dataclass, asdict

@dataclass
class Book:
    id: str = ""
    Title: str = ""
    subtitle: str = ""
    Author: str = ""
    Cover: str = ""
    Year: str = ""
    Isbn: str = ""
    Pages: str = ""
    Publisher: str = ""
    Categories: str = ""


Base = declarative_base()

engine = create_engine("sqlite:///search_cache.db")
Session = sessionmaker(bind=engine)

session = Session()


class Library(Base):
    __tablename__ = "library"
    id = Column(String, primary_key=True)
    Title = Column("Title", String, index=True)
    Subtitle = Column("Subtitle", String)
    Author = Column("Author", String)
    Isbn = Column("Isbn", String, nullable=True)
    Pages = Column("Pages", String, nullable=True)
    Year = Column("Year", String, nullable=True)
    Publisher = Column("Publisher", String, nullable=True)
    Categories = Column("Categories", String, nullable=True)

    def __init__(self, book: Book):
        self.Title = book.Title
        self.id = book.id
        self.Subtitle = Book.subtitle
        self.Author = book.Author
        self.Isbn = book.Isbn
        self.Pages = book.Pages
        self.Year = book.Year
        self.Publisher = book.Publisher
        self.Categories = book.Categories
    def __str__(self):
        return f'{self.Author} {self.Title} {self.Categories} {self.id}'


Base.metadata.create_all(engine)
