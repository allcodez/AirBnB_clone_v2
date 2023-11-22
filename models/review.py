#!/usr/bin/python3
"""Defines the Review class."""

from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Column

class Review(BaseModel, Base):
    """Represents a review within a MySQL database.

    Inherits from SQLAlchemy Base and corresponds to the MySQL table 'reviews'.
    Attributes:
        __tablename__ (str): The name of the MySQL table storing Review objects.
        text (sqlalchemy.String): The description of the Review.
        place_id (sqlalchemy.String): The ID of the Place associated with the Review.
        user_id (sqlalchemy.String): The ID of the User who created the Review.
    """
    __tablename__ = "reviews"
    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
