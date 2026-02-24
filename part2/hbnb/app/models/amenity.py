# app/models/amenity.py

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Represents an amenity that can be associated with places.

    Attributes:
        name (str): Name of the amenity.
        description (str): Description of the amenity.
        places (list): Places that include this amenity.
    """

    def __init__(self, name, description):
        """
        Initialize an Amenity instance.

        Args:
            name (str): Amenity name.
            description (str): Amenity description.

        Raises:
            ValueError: If validation fails.
        """
        super().__init__()

        self._validate_name(name)

        self.name = name
        self.description = description
        self.places = []

    def _validate_name(self, name):
        """Validate name presence and length."""
        if not name or len(name) > 50:
            raise ValueError("name is required and must be <= 50 characters")

    def add_place(self, place):
        """
        Associate this amenity with a place.

        Args:
            place (Place): Place instance.
        """
        self.places.append(place)
        place.add_amenity(self)
        self.save()
