"""
User Repository module.

Extends SQLAlchemyRepository with User-specific queries.
Located in : app/persistance/repository/user_repository.py
"""

from app.models.user import User
from app.persistance.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository detected to User entity operations.

    Extends the generic SQLAlchemyRepository
    with user-specific queries like email lookup
    """

def __init__(self):
    super().__init__(User)

def get_user_by_email(self, email):
    """Retrieve a user by their email address.

    Args:
        email (str): The email to search for.

    Returns:
        User or None: The matching user, or None if not found.
    """
    return self.model.query.filter_by(email=email).first()
