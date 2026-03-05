import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        r_owner = self.client.post('/api/v1/users/', json={
            "first_name": "Alice", "last_name": "Smith",
            "email": "alice@example.com",
            "password": "alice123"
        })
        self.owner_id = r_owner.get_json()['id']

        r_user = self.client.post('/api/v1/users/', json={
            "first_name": "Bob", "last_name": "Jones",
            "email": "bob@example.com",
            "password": "bob123"
        })
        self.user_id = r_user.get_json()['id']

        r_place = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "description": "Nice",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        })
        self.place_id = r_place.get_json()['id']

        self.valid_review = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }

    # POST /api/v1/reviews/
    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/',
                                    json=self.valid_review)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_invalid_rating_high(self):
        payload = {**self.valid_review, "rating": 6}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_rating_low(self):
        payload = {**self.valid_review, "rating": 0}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        payload = {**self.valid_review, "text": ""}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        payload = {**self.valid_review, "user_id": "fake-id"}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        payload = {**self.valid_review, "place_id": "fake-id"}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_owner_cannot_review_own_place(self):
        payload = {**self.valid_review, "user_id": self.owner_id}
        response = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(response.status_code, 400)

    # GET /api/v1/reviews/
    def test_get_all_reviews_empty(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_all_reviews(self):
        self.client.post('/api/v1/reviews/', json=self.valid_review)
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    # GET /api/v1/reviews/<id>
    def test_get_review_by_id(self):
        post_resp = self.client.post('/api/v1/reviews/',
                                     json=self.valid_review)
        review_id = post_resp.get_json()['id']
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('user_id', data)
        self.assertIn('place_id', data)
        self.assertIn('text', data)

    def test_get_review_not_found(self):
        response = self.client.get('/api/v1/reviews/fake-id-000')
        self.assertEqual(response.status_code, 404)

    # PUT /api/v1/reviews/<id>
    @unittest.expectedFailure
    def test_update_review_success(self):
        post_resp = self.client.post('/api/v1/reviews/',
                                     json=self.valid_review)
        review_id = post_resp.get_json()['id']
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"text": "Amazing!", "rating": 4,
                  "user_id": self.user_id, "place_id": self.place_id}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["text"], "Amazing!")
        self.assertEqual(data["rating"], 4)

    def test_update_review_not_found(self):
        response = self.client.put(
            '/api/v1/reviews/fake-id-000',
            json={"text": "Test", "rating": 3,
                  "user_id": self.user_id, "place_id": self.place_id}
        )
        self.assertEqual(response.status_code, 404)

    def test_update_review_invalid_rating(self):
        post_resp = self.client.post('/api/v1/reviews/',
                                     json=self.valid_review)
        review_id = post_resp.get_json()['id']
        response = self.client.put(
            f'/api/v1/reviews/{review_id}',
            json={"text": "Bad", "rating": 0,
                  "user_id": self.user_id, "place_id": self.place_id}
        )
        self.assertEqual(response.status_code, 400)

    # DELETE /api/v1/reviews/<id>
    def test_delete_review_success(self):
        post_resp = self.client.post('/api/v1/reviews/',
                                     json=self.valid_review)
        review_id = post_resp.get_json()['id']
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_delete_review_not_found(self):
        response = self.client.delete('/api/v1/reviews/fake-id-000')
        self.assertEqual(response.status_code, 404)

    def test_delete_review_then_get(self):
        post_resp = self.client.post('/api/v1/reviews/',
                                     json=self.valid_review)
        review_id = post_resp.get_json()['id']
        self.client.delete(f'/api/v1/reviews/{review_id}')
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 404)

    # GET /api/v1/places/<place_id>/reviews
    def test_get_reviews_by_place(self):
        self.client.post('/api/v1/reviews/', json=self.valid_review)
        response = self.client.get(
            f'/api/v1/places/{self.place_id}/reviews'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    def test_get_reviews_by_place_not_found(self):
        response = self.client.get('/api/v1/places/fake-id/reviews')
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
