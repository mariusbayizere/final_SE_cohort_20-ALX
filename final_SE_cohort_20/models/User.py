# from sqlalchemy import Column, String
# from sqlalchemy.orm import relationship
# from .base import Base

# class User(Base):
#     __tablename__ = 'users'
#     user_id = Column(String(8), primary_key=True, unique=True)
#     firstname = Column("First Name", String(50), nullable=False)
#     lastname = Column("Last Name", String(50), nullable=False)
#     email = Column(String(100), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)
#     address = Column("Address", String(255), nullable=False)
#     phone_number = Column("Phone Number", String(20), nullable=False, unique=True)
    
#     # Relationship to Books
#     books = relationship('Books', back_populates='user',cascade="all")
#     borrows = relationship('Borrow', back_populates='user',cascade="all, delete-orphan")


from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base
from . import db

# class User(Base):
# class User(db.Model, UserMixin):
#     __tablename__ = 'users'
#     user_id = Column(String(8), primary_key=True, unique=True)
#     firstname = Column("First Name", String(50), nullable=False)
#     lastname = Column("Last Name", String(50), nullable=False)
#     email = Column(String(100), nullable=False, unique=True)
#     password = Column(String(255), nullable=False)
#     UserRole = Column("UserRole", String(255), nullable=True)
#     address = Column("Address", String(255), nullable=False)
#     phone_number = Column("Phone Number", String(20), nullable=False, unique=True)
    
#     # Relationship to Books
#     books = relationship('Books', back_populates='user', cascade="all")
    
#     # Relationship to Borrow
#     borrows = relationship('Borrow', back_populates='user', cascade="all, delete-orphan")


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = Column(String(8), primary_key=True, unique=True)
    firstname = Column("First Name", String(50), nullable=False)
    lastname = Column("Last Name", String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    UserRole = Column("UserRole", String(255), nullable=True)
    address = Column("Address", String(255), nullable=False)
    phone_number = Column("Phone Number", String(20), nullable=False, unique=True)
    
    # Relationship to Books
    books = relationship('Books', back_populates='user', cascade="all")
    
    # Relationship to Borrow
    borrows = relationship('Borrow', back_populates='user', cascade="all, delete-orphan")
    
    # This method is required by Flask-Login
    def get_id(self):
        return self.user_id  # Use 'user_id' as the unique identifier