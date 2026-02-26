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
        """Initialize repositories for users, places, reviews, and amenities."""
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

    def update_user(self, user_id, user_data):
        """Update an existing user."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if "first_name" in user_data:
            user._validate_name(user_data["first_name"], "first_name")
            user.first_name = user_data["first_name"]
        if "last_name" in user_data:
            user._validate_name(user_data["last_name"], "last_name")
            user.last_name = user_data["last_name"]
        if "email" in user_data:
            existing = self.get_user_by_email(user_data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already exists")
            user._validate_email(user_data["email"])
            user.email = user_data["email"]
        if "password" in user_data:
            user._validate_password(user_data["password"])
            user.set_password(user_data["password"])

        user.save()
        return user

    # ==================================================
    # PLACE METHODS
    # ==================================================

    def create_place(self, place_data):
        """
        Create a new place, linking owner and amenities.

        Args:
            place_data (dict): Dictionary containing place fields:
                - title (str)
                - description (str)
                - price (float)
                - latitude (float)
                - longitude (float)
                - owner_id (str)
                - amenities (list of str, optional)

        Returns:
            Place: The created Place instance.

        Raises:
            ValueError: If owner not found, amenities not found, or validation fails.
        """
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        # Create the Place instance
        place = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner,
        )

        # Attach amenities if provided
        for amenity_id in place_data.get("amenities", []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a place by ID.

        Args:
            place_id (str): ID of the place.

        Returns:
            Place or None: The Place instance or None if not found.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all places.

        Returns:
            list[Place]: List of all Place instances.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update an existing place's information.

        Args:
            place_id (str): ID of the place to update.
            place_data (dict): Dictionary containing fields to update.

        Returns:
            Place or None: The updated Place instance, or None if not found.

        Raises:
            ValueError: If validation fails or amenities not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Update title, description, price, latitude, longitude
        if "title" in place_data:
            if not place_data["title"] or len(place_data["title"]) > 100:
                raise ValueError("title is required and must be <= 100 characters")
            place.title = place_data["title"]
        if "description" in place_data:
            place.description = place_data["description"]
        if "price" in place_data:
            place.price = place_data["price"]  # setter validates
        if "latitude" in place_data:
            place.latitude = place_data["latitude"]  # setter validates
        if "longitude" in place_data:
            place.longitude = place_data["longitude"]  # setter validates

        # Update amenities if provided
        if "amenities" in place_data:
            place.amenities = []
            for amenity_id in place_data["amenities"]:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity {amenity_id} not found")
                place.add_amenity(amenity)

        place.save()
        return place

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

        if user.id == place.owner.id:
            raise ValueError("Owner cannot review their own place")

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

    def get_reviews(self):
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

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): ID of the amenity to update.
            amenity_data (dict): Dictionary containing fields to update.

        Returns:
            Amenity or None: Updated Amenity instance or None if not found.

        Raises:
            ValueError: If validation fails.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        if "name" in amenity_data:
            if not amenity_data["name"]:
                raise ValueError("Name cannot be empty")
            amenity.name = amenity_data["name"]
        if "description" in amenity_data:
            amenity.description = amenity_data["description"]
        amenity.save()
        return amenity

    def delete_amenity(self, amenity_id):
        """Delete amenity."""
        return self.amenity_repo.delete(amenity_id)
