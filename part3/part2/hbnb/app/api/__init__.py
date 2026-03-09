"""
API package initialization.

This module creates the main Flask Blueprint used to group
all API routes of the HBnB application.

The blueprint defines the base URL prefix for the API.
Version-specific routes are registered in sub-packages
(e.g., api.v1).
"""

from flask import Blueprint

# Main API Blueprint
api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)

# Import versioned API to register namespaces
from app.api import v1  # noqa: E402,F401
