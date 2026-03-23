# app/models/user.py
import re
import hashlib
from app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the HBnB system.

    Attributes:
        first_name (str): First name of the user, max 50 characters.
        last_name (str): Last name of the user, max 50 characters.
        email (str): User's email address, must be valid format.
        password_hash (str): SHA256 hash of the user's password.
        is_admin (bool): Indicates if the user has admin privileges.
        places (list): List of Place instances owned by the user.
        reviews (list): List of Review instances written by the user.
    """

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        """
        Initialize a User instance with required attributes.

        Args:
            first_name (str): User's first name.
            last_name (str): User's last name.
            email (str): User's email address.
            password (str): User's password.
            is_admin (bool, optional): Admin flag. Defaults to False.

        Raises:
            ValueError: If any validation fails.
        """
        super().__init__()
        self._validate_name(first_name, "first_name")
        self._validate_name(last_name, "last_name")
        self._validate_email(email)
        self._validate_password(password)
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a boolean")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.is_admin = is_admin

        self.places = []
        self.reviews = []

    # -------------------
    # Validation Methods
    # -------------------
    def _validate_name(self, value, field_name):
        """
        Validate that a name attribute is present and <= 50 characters.

        Args:
            value (str): The name to validate.
            field_name (str): The name of the attribute (first_name/last_name).

        Raises:
            ValueError: If validation fails.
        """
        if not value or len(value) > 50:
            raise ValueError(f"{field_name} is required and must be <= 50 characters")

    def _validate_email(self, email):
        """
        Validate the email format.

        Args:
            email (str): Email to validate.

        Raises:
            ValueError: If email is missing or invalid.
        """
        if not email:
            raise ValueError("email is required")
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

    def _validate_password(self, password):
        """
        Validate the password length.

        Args:
            password (str): Password to validate.

        Raises:
            ValueError: If password is too short.
        """
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

    # -------------------
    # Password Handling
    # -------------------
    def set_password(self, password: str):
        """
        Hash the password and store it in password_hash.

        Args:
            password (str): Plain-text password.
        """
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """
        Check if the given password matches the stored hash.

        Args:
            password (str): Plain-text password to check.

        Returns:
            bool: True if password matches, False otherwise.
        """
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    # -------------------
    # Business Methods
    # -------------------
    def register(self, first_name, last_name, email, password):
        """
        Register or update user information with password.

        Args:
            first_name (str): First name.
            last_name (str): Last name.
            email (str): Email address.
            password (str): Plain-text password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)

    def update_profile(self, first_name, last_name, email):
        """
        Update the user's profile information.

        Args:
            first_name (str): New first name.
            last_name (str): New last name.
            email (str): New email address.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.save()

    def change_password(self, new_password):
        """
        Change the user's password.

        Args:
            new_password (str): New plain-text password.
        """
        self.set_password(new_password)
        self.save()

    def delete_account(self):
        """
        Placeholder method for deleting a user account.

        Actual deletion will be handled via the Facade/Repository layer.
        """
        pass

    # -------------------
    # Relationship Helpers
    # -------------------
    def add_place(self, place):
        """
        Add a place to the user's list of owned places.

        Args:
            place (Place): Place instance to add.
        """
        self.places.append(place)
        self.save()

    def add_review(self, review):
        """
        Add a review to the user's list of reviews.

        Args:
            review (Review): Review instance to add.
        """
        self.reviews.append(review)
        self.save()
