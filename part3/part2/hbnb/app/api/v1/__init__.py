"""
API v1 initialization.

This module creates and configures the Flask-RESTx API
instance for version 1 of the HBnB application.

It registers all available namespaces such as:
- Users
- Places
- Reviews
- Amenities

All routes defined in this version will be prefixed with:
    /api/v1/
"""

from flask_restx import Api
from app.api import api_bp

# Import namespaces
from app.api.v1.users import api as users_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.amenities import api as amenities_ns


# Create RESTx API instance
api = Api(
    api_bp,
    version="1.0",
    title="HBnB API",
    description="HBnB Application REST API (Version 1)",
    doc="/"
)

# Register namespaces with version prefix
api.add_namespace(users_ns, path="/v1/users")
api.add_namespace(places_ns, path="/v1/places")
api.add_namespace(reviews_ns, path="/v1/reviews")
api.add_namespace(amenities_ns, path="/v1/amenities")
