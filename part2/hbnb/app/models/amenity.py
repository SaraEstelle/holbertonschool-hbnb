from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name must be a non-empty string")
        self.name = name.strip()
