"""
Amenity Repository module.

Extends SQLAlchemyRepository with amenity-specific queries.
Located in: app/persitence/repositories/amenity_repository.py
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Repository dedicated to Amenity entity operations."""

    def __init__(self):
        super().__init__(Amenity)

    def get_amentiy_by_name(self, name):
        """Retrieve an amenity by its name."""
        return self.model.query.filter_by(name=name).first()
