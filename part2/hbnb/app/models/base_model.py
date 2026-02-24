import uuid
from datetime import datetime


class BaseModel:
    """
    Base class for all models.
    Handles common attributes: id, created_at, updated_at.
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def save(self):
        """
        Updates the updated_at timestamp.
        Should be called whenever the object is modified.
        """
        self.updated_at = datetime.utcnow()

    def update(self, data: dict):
        """
        Update object attributes from a dictionary.
        Only updates existing attributes.
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ["id", "created_at"]:
                setattr(self, key, value)

        self.save()
