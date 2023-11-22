#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Column

class City(BaseModel, Base):
    """Represents a city within a MySQL database.

    Inherits from SQLAlchemy Base and corresponds to the MySQL table 'cities'.

    Attributes:
        __tablename__ (str): The name of the MySQL table storing City objects.
        name (sqlalchemy.String): The name of the City.
        state_id (sqlalchemy.String): The state ID associated with the City.
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
