"""
Place Repository module.

Extends SQLAchemyRepository with Place-specific queries.
Located in: app/persistence/repositories/place_repository.py
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository dedicated to Place entity operations."""

    def __init__(self):
        super().__init__(Place)

    def get_places_by_owner(self, owner_id):
        """Retrienve all places owned by a specific user."""
        return self.model.query.filter_by(owner_id=owner_id).all()
