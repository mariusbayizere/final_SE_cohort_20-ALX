from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .User import User
from .Books import Books
from .Borrowed import Borrow
