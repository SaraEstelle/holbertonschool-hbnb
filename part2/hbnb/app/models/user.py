import re
from app.models.base_model import BaseModel


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if not first_name or not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError("first_name must be a non-empty string (max 50 chars)")
        if not last_name or not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError("last_name must be a non-empty string (max 50 chars)")
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            raise ValueError("Invalid email format")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
