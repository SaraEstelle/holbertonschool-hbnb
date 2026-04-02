"""
Place API module.

This module defines the RESTful endpoints for managing Place objects
in the HBnB application. It provides CRUD operations (excluding DELETE)
and integrates with the business logic layer via the HBnBFacade.

Acces rules:
- POST /    : Authenticated (owner_id = current user)
- GET /     : Public
- GET /<id> : Public
- GET /<id> : Owner OR Admin
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# -----------------------------
# Related entity models
# -----------------------------

amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# -----------------------------
# Place input model
# -----------------------------

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'amenities': fields.List(fields.String, description="List of amenities ID's")
})

# -----------------------------
# Place list endpoints
# -----------------------------

@api.route('/')
class PlaceList(Resource):

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new place. Requires authentication."""
        current_user = get_jwt_identity()

        place_data = api.payload
        # owner_id is set from the JWT token - not from the request body
        place_data['owner_id'] = current_user

        try:
            place = facade.create_place(place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places. Public endpoint."""
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'latitude': p.latitude,
                'longitude': p.longitude
            }
            for p in places
        ], 200

# -----------------------------
# Single place endpoints
# -----------------------------

@api.route('/<place_id>')
class PlaceResource(Resource):

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID, including owner and amenities.Public endpoint."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        owner = facade.get_user(place.owner.id)
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            } if owner else None,
            'amenities': [{'id': a.id, 'name': a.name} for a in place.amenities]
        }, 200

    @jwt_required()
    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information. Only the owner can modify it."""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Admin bypasses ownership check
        if not is_admin and place.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        place_data.pop('owner_id', None)  # Ensure owner_id cannot be modified

        try:
            facade.update_place(place_id, place_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {'message': 'Place updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place. Only the owner can delete it."""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Admin bypasses ownership check
        if not is_admin and place.owner.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_place(place_id)
        return {'message': 'Place deleted successfully'}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place. Public endpoint."""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)

        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            "place_id": review.place.id
        } for review in reviews], 200
