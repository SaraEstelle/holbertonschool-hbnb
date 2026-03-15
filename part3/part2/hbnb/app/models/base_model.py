"""
Base model module

Defines the BaseModel class mapped to SQLAlchemy
All other models inherits from this class.
"""

import uuid
from datetime import datetime, timezone
from app import db


class BaseModel(db.model): # db.Model obligatoire pour SQLAlchemy mappe les tables
    """
    Classe de base pour tous les models SQLAlchemy.
    on met __abstract__ = True pour que SQLAlchemy ne cree pas de table pour BaseModel lui-meme.
    """

    __abstract__ = True # No table created for BaseModel itself

    id = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False
    )

    def save(self):
        """
        Updates the updated_at timestamp.
        Should be called whenever the object is modified.
        """
        self.updated_at = datetime.now(timezone.utc)
        db.session.commit()

    def update(self, data: dict):
        """
        Update object attributes from a dictionary.
        Only updates existing attributes.
        ignored id and created_at pour pas les ecraser.
        """
        for key, value in data.items():
            if hasattr(self, key) and key not in ["id", "created_at"]:
                setattr(self, key, value)
        self.save()
