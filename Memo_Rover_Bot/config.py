DATABASE_URL = 'postgresql://Username:Password@localhost:5432/Database'
#                ^^^^^^^^^^^fill in the details ^^^^^^^^^^^^
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    text = Column(String)


