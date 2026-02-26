"""
Services package.

This module initializes the HBnBFacade instance,
which acts as the entry point to the business logic layer.
"""

from app.services.facade import HBnBFacade

facade = HBnBFacade()

__all__ = ["facade", "HBnBFacade"]
