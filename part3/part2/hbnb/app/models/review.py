# app/models/review.py

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review written by a user for a place.

    Attributes:
        rating (int): Rating between 1 and 5.
        text (str): Review text text.
        user (User): Author of the review.
        place (Place): Place being reviewed.
    """

    def __init__(self, text, rating, user, place):
        """
        Initialize a Review instance.

        Args:
            rating (int): Rating value (1–5).
            text (str): Comment text.
            user (User): Author of review.
            place (Place): Reviewed place.

        Raises:
            ValueError: If validation fails.
        """
        super().__init__()

        self._validate_rating(rating)

        if user is None:
            raise ValueError("user is required")

        if place is None:
            raise ValueError("place is required")

        if not text or text.strip() == "":
            raise ValueError("text is required")
        self.text = text
        self.rating = int(rating)
        self.user = user
        self.place = place

        user.add_review(self)
        place.add_review(self)

    def _validate_rating(self, rating):
        """Validate rating is between 1 and 5."""
        if not (1 <= int(rating) <= 5):
            raise ValueError("rating must be between 1 and 5")
