"""
Review API module.

This module defines the RESTful endpoints for managing Review objects
in the Hbnb application. Protected endpoints require JWT authentication.

Access rules:
- POST /    : Authenticated (user_id = current user, not own place, not duplicate)
- GET /    : Public
- GET /<id>    : Author OR Admin
- DELETE /<id>  :Author OR Admin
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Written feedback'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=True, description='Written feedback'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new review. Requires authentication."""
        current_user = get_jwt_identity()


        review_data = api.payload
        # user_id comes from JWT - not from the request body
        review_data['user_id'] = current_user

        if not review_data.get('text') or review_data['text'].strip() == '':
            return{'error': 'Text cannot be empty'}, 400

        if review_data['rating'] < 1 or review_data['rating'] > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400

        # Check the place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            return{'error': 'Place not found'}, 404

        #check user is not reviewing their own place
        if place.owner.id == current_user:
            return{'error': 'You cannot review your own place'}, 400

        #Cannot review the same place twice
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for r in existing_reviews:
            if r.user.id == current_user:
                return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': current_user,
                'place_id': review_data['place_id']
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews. Public endpoint."""
        reviews = facade.get_all_reviews()
        return [{
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        } for review in reviews], 200


@api.route('/<review_id>')
class ReviewResource(Resource):

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID. Public endpoint."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            "user_id": review.user.id,
            "place_id": review.place.id
        }, 200

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review. Only the author can modify it."""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Admin bypasses ownership check
        if not is_admin and review.user.id !=current_user:
            return {'error': 'Unauthorized action'}, 403

        update_data = api.payload
        if update_data['rating'] < 1 or update_data['rating'] > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400

        try:
            facade.update_review(review_id, update_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review. Only the author can delete it."""
        current_user = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Admin bypasses ownership check
        if not is_admin and review.user.id != current_user:
            return {'error': 'Unauthorized action'}, 403

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200
