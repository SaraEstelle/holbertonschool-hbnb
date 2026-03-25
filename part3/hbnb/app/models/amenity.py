# app/models/amenity.py

from app import db
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with places.

    Attributes:
        name (str): Name of the amenity.
        description (str): Description of the amenity.
        places (list): Places that include this amenity.
    """

    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text,  nullable=True, default='')


    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("name is required and must be <= 50 characters")
        return value
