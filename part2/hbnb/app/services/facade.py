# app/services/facade.py

from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade layer acting as the single entry point
    between the API layer and the business logic layer.
    """

    def __init__(self):
        """Initialize repositories."""
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ==================================================
    # USER METHODS
    # ==================================================

    def create_user(self, user_data):
        """
        Create a new user.

        Args:
            user_data (dict): Dictionary containing user fields.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If email already exists.
        """
        if self.get_user_by_email(user_data["email"]):
            raise ValueError("Email already exists")

        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
            is_admin=user_data.get("is_admin", False),
        )

        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Retrieve a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Retrieve a user by email."""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def delete_user(self, user_id):
        """Delete a user by ID."""
        return self.user_repo.delete(user_id)

    # ==================================================
    # PLACE METHODS
    # ==================================================

    def create_place(self, place_data):
        """
        Create a new place.

        Args:
            place_data (dict): Dictionary containing place fields.

        Returns:
            Place: The created place instance.

        Raises:
            ValueError: If owner or amenities not found.
        """
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner,
        )

        # Attach amenities (many-to-many)
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places."""
        return self.place_repo.get_all()

    def delete_place(self, place_id):
        """Delete a place."""
        return self.place_repo.delete(place_id)

    # ==================================================
    # REVIEW METHODS
    # ==================================================

    def create_review(self, review_data):
        """
        Create a new review.

        Args:
            review_data (dict): Dictionary containing review fields.

        Returns:
            Review: The created review instance.

        Raises:
            ValueError: If user or place not found.
        """
        user = self.user_repo.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            rating=review_data["rating"],
            comment=review_data.get("comment", ""),
            user=user,
            place=place,
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews."""
        return self.review_repo.get_all()

    def delete_review(self, review_id):
        """Delete review."""
        return self.review_repo.delete(review_id)

    # ==================================================
    # AMENITY METHODS
    # ==================================================

    def create_amenity(self, amenity_data):
        """
        Create a new amenity.

        Args:
            amenity_data (dict): Dictionary containing amenity fields.

        Returns:
            Amenity: The created amenity instance.
        """
        amenity = Amenity(
            name=amenity_data["name"],
            description=amenity_data.get("description", ""),
        )

        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Retrieve amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Retrieve all amenities."""
        return self.amenity_repo.get_all()

    def delete_amenity(self, amenity_id):
        """Delete amenity."""
        return self.amenity_repo.delete(amenity_id)
