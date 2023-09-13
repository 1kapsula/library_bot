from sqlalchemy import Integer, String, \
    Column, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    book_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(DateTime, nullable=False)
    date_deleted = Column(DateTime, nullable=True)


class Borrow(Base):
    __tablename__ = 'borrows'

    borrow_id = Column(Integer, primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey("books.book_id"))
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=True)
    user_id = Column(Integer, nullable=False)
    book = relationship("Book", cascade="all, delete-orphan")
