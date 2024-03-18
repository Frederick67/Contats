from sqlalchemy import create_engine, Column, Integer, String, Text, Sequence, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(String(50))
    email = Column(String(50))