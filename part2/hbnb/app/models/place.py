"""
Place model module.

This module defines the Place class used in the HBnB application.
A Place represents a property listed by a user and can have
multiple amenities and reviews associated with it.
"""

from app.models.base_model import BaseModel


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

    def __init__(self, title, description, price,
                 latitude, longitude, owner):
        """
        Initialize a Place instance.

        Args:
            title (str): Title of the place.
            description (str): Description text.
            price (float): Price per night (must be non-negative).
            latitude (float): Latitude (-90 to 90).
            longitude (float): Longitude (-180 to 180).
            owner (User): Owner of the place.

        Raises:
            ValueError: If validation fails.
        """
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError(
                "title is required and must be <= 100 characters"
            )

        if owner is None:
            raise ValueError("owner is required")

        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews = []
        self.amenities = []

        # Maintain bidirectional relationship
        owner.add_place(self)

    # ==================================================
    # Property: price
    # ==================================================

    @property
    def price(self):
        """Get the price per night."""
        return self._price

    @price.setter
    def price(self, value):
        """
        Set the price per night.

        Args:
            value (float): New price value.

        Raises:
            ValueError: If price is negative.
        """
        if value is None or float(value) < 0:
            raise ValueError("price must be a non-negative number")
        self._price = float(value)

    # ==================================================
    # Property: latitude
    # ==================================================

    @property
    def latitude(self):
        """Get the latitude."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """
        Set the latitude.

        Args:
            value (float): Latitude value.

        Raises:
            ValueError: If latitude is out of range.
        """
        if not (-90 <= float(value) <= 90):
            raise ValueError(
                "latitude must be between -90 and 90"
            )
        self._latitude = float(value)

    # ==================================================
    # Property: longitude
    # ==================================================

    @property
    def longitude(self):
        """Get the longitude."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """
        Set the longitude.

        Args:
            value (float): Longitude value.

        Raises:
            ValueError: If longitude is out of range.
        """
        if not (-180 <= float(value) <= 180):
            raise ValueError(
                "longitude must be between -180 and 180"
            )
        self._longitude = float(value)

    # ==================================================
    # Relationship methods
    # ==================================================

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
