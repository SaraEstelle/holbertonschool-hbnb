"""
Amenity model module.

Mappe l'entite Amenity sur la table 'amenities' via SQLAlchemy.
"""

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class Review(BaseModel):
    """
    Represents a review written by a user for a place.

    Attributes:
        rating (int): Rating between 1 and 5.
        text (str): Review text text.
        user (User): Author of the review.
        place (Place): Place being reviewed.
    """

    __tablename__ = 'reviews'

    text = db.Column(db.Text,  nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    #-----------------------
    # SQLAlchemy Validators
    #-----------------------


    @validates('text')
    def validate_text(self, key, value):
        if not value or value.strip() == '' :
            raise ValueError("text is required")
        return value

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= int(value) <= 5):
            raise ValueError("rating must be between 1 and 5")
        return int(value)
    
    #-------------------
    # SQL Relation
    #-------------------

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
