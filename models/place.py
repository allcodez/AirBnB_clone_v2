#!/usr/bin/python3
"""Defines the Place class."""

from os import getenv
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from sqlalchemy import Table
from models.review import Review
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Column

association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))

class Place(BaseModel, Base):
    """Represents a Place within a MySQL database.

    Inherits from SQLAlchemy Base and corresponds to the MySQL table 'places'.

    Attributes:
        __tablename__ (str): The name of the MySQL table storing Place objects.
        city_id (sqlalchemy.String): The city ID associated with the Place.
        user_id (sqlalchemy.String): The user ID associated with the Place.
        name (sqlalchemy.String): The name of the Place.
        description (sqlalchemy.String): The description of the Place.
        number_rooms (sqlalchemy.Integer): The number of rooms in the Place.
        number_bathrooms (sqlalchemy.Integer): The number of bathrooms in the Place.
        max_guest (sqlalchemy.Integer): The maximum number of guests in the Place.
        price_by_night (sqlalchemy.Integer): The price per night for the Place.
        latitude (sqlalchemy.Float): The latitude of the Place.
        longitude (sqlalchemy.Float): The longitude of the Place.
        reviews (sqlalchemy.relationship): Relationship with the Review model.
        amenities (sqlalchemy.relationship): Relationship with the Amenity model.
        amenity_ids (list): A list of IDs for linked amenities.
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity", viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Retrieve a list of all linked Reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked all Amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
