"""
Persistence package.

This module exposes repository implementations used
to handle data storage for the HBnB application.
"""

from app.persistence.repository import InMemoryRepository

__all__ = ["InMemoryRepository"]
