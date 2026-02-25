"""
Amenity API endpoints module.

This module defines the RESTful endpoints for managing amenities
in the HBnB application. It handles creation, retrieval, and update
operations for amenities through the Facade layer.
"""

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """
    Resource for managing amenity collection.

    Provides endpoints to create a new amenity and
    retrieve all amenities.
    """

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Create a new amenity.

        Expects a JSON payload containing:
            - name (str): Name of the amenity

        Returns:
            dict: The created amenity's ID and name
            int: HTTP status code 201 on success

        Raises:
            400 Bad Request: If input data is invalid
        """
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_amenity.id,
            'name': new_amenity.name
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
                'name': a.name
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
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
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
        amenity_data = api.payload

        try:
            amenity = facade.update_amenity(amenity_id, amenity_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        if not amenity:
            return {'error': 'Amenity not found'}, 404

        return {'message': 'Amenity updated successfully'}, 200
