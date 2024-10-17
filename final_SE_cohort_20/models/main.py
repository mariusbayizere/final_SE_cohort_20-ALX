from sqlalchemy import create_engine
# from . import User, Books, Borrow
# from models.base import Base
from base import Base

connection = "mysql+pymysql://root:auca%402023@localhost/final_project_ALX"
engine = create_engine(connection)

Base.metadata.create_all(engine)
