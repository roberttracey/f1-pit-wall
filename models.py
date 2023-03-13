from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import validates

from app import db


class Circuits(db.Model):
    __tablename__ = 'circuits'
    circuitId = Column(Integer, primary_key=True)
    circuitRef = Column(String(255))
    name = Column(String(255))
    location = Column(String(255))
    country = Column(String(255))
    lat = Column(Float)
    lng = Column(Float)
    alt = Column(Integer)
    url = Column(Integer)

    def __str__(self):
        return self.name

class Constructors(db.Model):
    __tablename__ = 'constructors'
    constructorId = Column(Integer, primary_key=True)
    constructorRef = Column(String(255))
    name = Column(String(255))
    nationality = Column(String(255))
    url = Column(String(255))

    def __str__(self):
        return self.name
