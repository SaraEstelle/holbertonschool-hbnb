from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Written feedback'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(422, 'Business rule violation')
    @api.response(409, 'Conflict (duplicate review)')
    def post(self):
        """Create a new review"""

        review_data = api.payload

        required_fields = ["text", "rating", "user_id", "place_id"]
        for field in required_fields:
            if field not in review_data:
                return {"error": f"{field} is required"}, 400

        if not review_data["text"] or review_data["text"].strip() == "":
            return {"error": "Text cannot be empty"}, 400

        if review_data["rating"] < 1 or review_data["rating"] > 5:
            return {"error": "Rating must be between 1 and 5"}, 400

        try:
            new_review = facade.create_review(review_data)

            return {
                "id": new_review.id,
                "text": new_review.text,
                "rating": new_review.rating,
                "user_id": review_data["user_id"],
                "place_id": review_data["place_id"]
            }, 201

        except ValueError as e:
            return {"error": str(e)}, 400


    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""

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
        """Get review details by ID"""

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


    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(422, 'Business rule violation')
    def put(self, review_id):
        """Update a review"""

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        update_data = api.payload

        if update_data['rating'] < 1 or update_data['rating'] > 5:
            return {'error': 'Rating must be between 1 and 5'}, 400

        try:
            facade.update_review(review_id, update_data)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        facade.delete_review(review_id)

        return {'message': 'Review deleted successfully'}, 200
