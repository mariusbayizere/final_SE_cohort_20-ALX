from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from . import db
from .base import Base

# class Books(Base):
class Books(db.Model):
    __tablename__ = 'books'
    book_id = Column(String(8), primary_key=True)
    title = Column(String(255), nullable=False, unique=True)
    Rating = Column(Integer, nullable=True)
    BookImages = Column(String(255), nullable=False)
    Description = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publication_year = Column(String(10), nullable=False)
    page = Column(Integer, nullable=False)
    book_status = Column(String(255), nullable=False, default='Available')

    # Foreign key
    user_id = Column(String(8), ForeignKey('users.user_id'))
    
    # Relationships
    user = relationship('User', back_populates='books')  # Relationship to User
    borrows = relationship('Borrow', back_populates='books', cascade="all, delete-orphan")
