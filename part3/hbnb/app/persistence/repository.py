"""
Repository module.

contains:
- Repository : Abstract base class defining the interface
- InMemoryRepository : In-memory implementation (kept for testing)
- SQLAlechemyRepository :  SQLAlchemy-based implementation for persistence
"""

from abc import ABC, abstractmethod


# =================================
# Abstract Base Repository
# =================================

class Repository(ABC):

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


# ================================================
# In-Memory Repository (Kept for tests / fallback)
# ================================================

class InMemoryRepository(Repository):

    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
            if getattr(obj, attr_name) == attr_value),
            None
        )


# ===================================
# SQLAlchemy Repository
# ===================================

class SQLAlchemyRepository(Repository):
    """SQLAlechemy-based repository implementing the Repository interface.

    Handles all CRUD operations through SQLAlchemy sessiosn.
    Can be used for any mapped model (User, Place,Review, Amenity).
    """


    def __init__(self, model):
        """Args:
                model: The SQLAlchemy model class to manage (like User, Place).
                    """
        from app import db
        self.model = model
        self.db = db

    def add(self, obj):
        """Add a new object to the database."""
        self.db.session.add(obj)
        self.db.session.commit()

    def get(self, obj_id):
        """Retrieve an object by its primary key."""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Retrieve all objects of this model."""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object's attributes by ID."""
        obj =  self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            self.db.session.commit()


    def delete(self, obj_id):
        """Delete an object by ID."""
        obj = self.get(obj_id)
        if obj:
            self.db.session.delete(obj)
            self.db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        """Retrieve the first object matching a given attribute value."""
        return self.model.query.filter_by(
            **{attr_name: attr_value}
        ).first()
