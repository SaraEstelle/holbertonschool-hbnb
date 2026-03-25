# app/models/user.py
import re
from app import db, bcrypt
from app.models.base_model import BaseModel
from sqlalchemy.orm import validates

class User(BaseModel):
    """
    Represents a user in the HBnB system.

    Attributes:
        first_name (str): First name of the user, max 50 characters.
        last_name (str): Last name of the user, max 50 characters.
        email (str): User's email address, must be valid format.
        password (str): Bcrypt hash of the user's password.
        is_admin (bool): Indicates if the user has admin privileges.
        places (list): List of Place instances owned by the user.
        reviews (list): List of Review instances written by the user.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name  = db.Column(db.String(50), nullable=False)
    email      = db.Column(db.String(120), nullable=False, unique=True)
    password   = db.Column(db.String(128), nullable=False)
    is_admin   = db.Column(db.Boolean,     default=False)


    # ------------------------
    # SQLAlchemy Validators
    # ------------------------

    @validates('first_name')
    def validate_first_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("First_name is required and must be <= 50 characters")
        return value

    @validates('last_name')
    def validate_last_name(self, key, value):
        if not value or len(value) > 50:
            raise ValueError("last_name is required and must be <= 50 characters")
        return value

    @validates('email')
    def validate_email(self, key, value):
        if not value:
            raise ValueError("email is required")
        pattern =  r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format")
        return value

    # -------------------
    # Password Handling
    # -------------------

    def hash_password(self, password):
        """
        Hashes the password using bcrypt before storing it.

        Args:
            password (str): Plain-text password.
        """
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password.

        Args:
            password (str): Plain-text password to verify.

        Returns:
            bool: True if password matches, False otherwise.
        """
        return bcrypt.check_password_hash(self.password, password)

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
        self.hash_password(password)

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
        self.hash_password(new_password)
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

    #-------------------
    # SQL Relation 
    #-------------------

    places = db.relationship('Place', backref='owner')
    reviews = db.relationship('Review', backref='user')
