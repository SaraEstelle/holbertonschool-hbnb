import unittest
from app import create_app

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review_valid(self):
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Great!",
            "rating": 5,
            "user_id": "VALID_USER_ID",
            "place_id": "VALID_PLACE_ID"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Great!",
            "rating": 10,
            "user_id": "VALID_USER_ID",
            "place_id": "VALID_PLACE_ID"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_comment(self):
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "",
            "rating": 4,
            "user_id": "VALID_USER_ID",
            "place_id": "VALID_PLACE_ID"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_nonexistent_review(self):
        response = self.client.get('/api/v1/reviews/fake-id')
        self.assertEqual(response.status_code, 404)
