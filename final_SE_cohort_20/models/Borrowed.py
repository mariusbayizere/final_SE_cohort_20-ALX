# from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from .base import Base
# from . import db

# # class Borrow(Base):
# class Borrow(db.Model):
#     __tablename__ = 'borrow'
#     id = Column("ID", Integer, primary_key=True, unique=True)
    
#     book_id = Column(String(8), ForeignKey('books.book_id'))
#     books = relationship('Books', back_populates='borrows')
    
#     user_id = Column(String(8), ForeignKey('users.user_id'))
#     user = relationship('User', back_populates='borrows')
    
#     borrow_date = Column("Borrow Date", DateTime, default=datetime.utcnow, nullable=False)
#     return_date = Column("Return Date", DateTime, nullable=True)
#     fine = Column("Fine", Integer, nullable=True)
#     status = Column("Status", String(255), nullable=False, default="Pending")



from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from . import db

# class Borrow(Base):
class Borrow(db.Model):
    __tablename__ = 'borrow'
    id = Column("ID", Integer, primary_key=True, unique=True)
    
    book_id = Column(String(8), ForeignKey('books.book_id'))
    books = relationship('Books', back_populates='borrows')
    
    user_id = Column(String(8), ForeignKey('users.user_id'))
    user = relationship('User', back_populates='borrows')
    borrow_date = Column("Borrow Date", DateTime, default=datetime.utcnow, nullable=False)
    return_date = Column("Return Date", DateTime, nullable=True)
    actual_return_date = Column("Actual Return Date", DateTime, nullable=True)
    fine = Column("Fine", Integer, nullable=True)
    status = Column("Status", String(255), nullable=False, default="Pending")
