# app/models/place.py

from app.models.base_model import BaseModel


class Place(BaseModel):
    """
    Represents a place listed in the HBnB system.

    Attributes:
        title (str): Title of the place.
        description (str): Description of the place.
        price (float): Price per night.
        latitude (float): Geographic latitude.
        longitude (float): Geographic longitude.
        owner (User): Owner of the place.
        reviews (list): List of Review instances.
        amenities (list): List of Amenity instances.
    """

    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        """
        Initialize a Place instance.

        Args:
            title (str): Title of the place.
            description (str): Description text.
            price (float): Price per night (must be positive).
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            owner (User): Owner of the place.

        Raises:
            ValueError: If validation fails.
        """
        super().__init__()

        self._validate_title(title)
        self._validate_price(price)
        self._validate_coordinates(latitude, longitude)

        if owner is None:
            raise ValueError("owner is required")

        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner = owner

        self.reviews = []
        self.amenities = []

        owner.add_place(self)

    def _validate_title(self, title):
        """Validate title presence and length."""
        if not title or len(title) > 100:
            raise ValueError("title is required and must be <= 100 characters")

    def _validate_price(self, price):
        """Validate price is positive."""
        if price is None or float(price) <= 0:
            raise ValueError("price must be a positive number")

    def _validate_coordinates(self, latitude, longitude):
        """Validate latitude and longitude ranges."""
        if not (-90 <= float(latitude) <= 90):
            raise ValueError("latitude must be between -90 and 90")
        if not (-180 <= float(longitude) <= 180):
            raise ValueError("longitude must be between -180 and 180")

    def add_review(self, review):
        """
        Add a review to this place.

        Args:
            review (Review): Review instance.
        """
        self.reviews.append(review)
        self.save()

    def add_amenity(self, amenity):
        """
        Add an amenity to this place.

        Args:
            amenity (Amenity): Amenity instance.
        """
        self.amenities.append(amenity)
        self.save()
