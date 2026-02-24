from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        if not title or not isinstance(title, str) or len(title) > 100:
            raise ValueError("title must be a non-empty string (max 100 chars)")
        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("price must be a non-negative number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self._longitude = float(value)
