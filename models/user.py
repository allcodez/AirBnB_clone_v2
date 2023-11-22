#!/usr/bin/python3
"""Defines the User class."""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import Column

class User(BaseModel, Base):
    """Represents a user within a MySQL database.

    Inherits from SQLAlchemy Base and corresponds to the MySQL table 'users'.
    Attributes:
        __tablename__ (str): The name of the MySQL table storing User objects.
        email (sqlalchemy.String): The email address of the User.
        password (sqlalchemy.String): The password associated with the User.
        first_name (sqlalchemy.String): The first name of the User.
        last_name (sqlalchemy.String): The last name of the User.
        places (sqlalchemy.relationship): Relationship with the Place model.
        reviews (sqlalchemy.relationship): Relationship with the Review model.
    """
    __tablename__ = "users"
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
