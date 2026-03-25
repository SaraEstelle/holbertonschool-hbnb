"""
Place model module.

This module defines the Place class used in the HBnB application.
A Place represents a property listed by a user and can have
multiple amenities and reviews associated with it.
"""

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates
from app.models.sql_tables import place_amenity

class Place(BaseModel):
    """
    Represents a place listed in the HBnB system.

    Attributes:
        title (str): Title of the place (max 100 characters).
        description (str): Description of the place.
        price (float): Price per night (non-negative).
        latitude (float): Geographic latitude (-90 to 90).
        longitude (float): Geographic longitude (-180 to 180).
        owner (User): Owner of the place.
        reviews (list): List of associated Review instances.
        amenities (list): List of associated Amenity instances.
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text,  nullable=True, default='')
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)


    #------------------------
    # Validateurs SQLAlchemy
    #------------------------

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("title is required and must be <= 100 characters")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value is None or float(value) < 0:
            raise ValueError("price must be a non-negative number")
        return float(value)

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90 <= float(value) <= 90):
            raise ValueError("latitude must be between -90 and 90")
        return float(value)

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180 <= float(value) <= 180):
            raise ValueError("longitude must be between -180 and 180")
        return float(value)

    def add_review(self, review):
        """Add a review to this place."""
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        self.amenities.append(amenity)
        self.save()

    #-------------------
    # SQL Relation
    #-------------------

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship('Review', backref='place')
    amenities = db.relationship('Amenity', secondary='place_amenity', backref='places')
    