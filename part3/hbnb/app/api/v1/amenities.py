"""
Amenity API endpoints module.

This module defines the RESTful endpoints for managing amenities
in the HBnB application.

Access rules:
- POST /     : Admin only
- GET /     : Public
- GET /<id> : Public
- PUT/<amenity_id> : Admin only
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    """
    Resource for managing amenity collection.

    Provides endpoints to create a new amenity and
    retrieve all amenities.
    """

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """
        Create a new amenity. Admin only."""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name,
            'description': new_amenity.description
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve all amenities.

        Returns:
            list: A list of all amenities
            int: HTTP status code 200
        """
        amenities = facade.get_all_amenities()
        return [
            {
                'id': a.id,
                'name': a.name,
                'description': a.description
            }
            for a in amenities
        ], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    """
    Resource for managing a single amenity.

    Provides endpoints to retrieve or update
    an amenity by its ID.
    """

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Retrieve an amenity by ID.

        Args:
            amenity_id (str): The unique identifier of the amenity

        Returns:
            dict: The amenity details (id and name)
            int: HTTP status code 200 on success

        Raises:
            404 Not Found: If the amenity does not exist
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(403, 'Admin Privileges required')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an existing amenity.

        Args:
            amenity_id (str): The unique identifier of the amenity

        Expects:
            JSON payload containing:
                - name (str): Updated name of the amenity

        Returns:
            dict: Success message
            int: HTTP status code 200 on success

        Raises:
            400 Bad Request: If input data is invalid
            404 Not Found: If the amenity does not exist
        """
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error' : 'Admin privileges required'}, 403

        amenity_data = api.payload

        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(403, 'Admin Privileges required')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity. Admin only."""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error' :'Admin provileges required'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        facade.delete_amenity(amenity_id)
        return {'message': 'Amenity deleted successfully'}, 200
