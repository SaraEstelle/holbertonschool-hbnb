# app/models/review.py

from app.models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review written by a user for a place.

    Attributes:
        rating (int): Rating between 1 and 5.
        comment (str): Review comment text.
        user_id (str): ID of the user (optional for now).
        place_id (str): ID of the place (optional for now).
    """

    def __init__(self, rating, comment, user_id=None, place_id=None):
        super().__init__()

        self._validate_rating(rating)
        self._validate_comment(comment)

        self.rating = int(rating)
        self.comment = comment
        self.user_id = user_id
        self.place_id = place_id

    # -------------------
    # Validation Methods
    # -------------------

    def _validate_rating(self, rating):
        """Validate rating is between 1 and 5."""
        if not isinstance(rating, int):
            raise ValueError("rating must be an integer")

        if rating < 1 or rating > 5:
            raise ValueError("rating must be between 1 and 5")

    def _validate_comment(self, comment):
        """Validate comment is not empty."""
        if not comment or comment.strip() == "":
            raise ValueError("comment cannot be empty")
