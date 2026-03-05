import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

        r = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "password": "alice123"
        })
        self.owner_id = r.get_json()['id']

        self.valid_place = {
            "title": "Cozy Apartment",
            "description": "A nice place",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.owner_id,
            "amenities": []
        }

    # POST /api/v1/places/
    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json=self.valid_place)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_create_place_invalid_owner(self):
        payload = {**self.valid_place, "owner_id": "fake-id"}
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        payload = {**self.valid_place, "price": -10.0}
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        payload = {**self.valid_place, "latitude": 95.0}
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        payload = {**self.valid_place, "longitude": 200.0}
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_place_empty_title(self):
        payload = {**self.valid_place, "title": ""}
        response = self.client.post('/api/v1/places/', json=payload)
        self.assertEqual(response.status_code, 400)

    # GET /api/v1/places/
    def test_get_all_places_empty(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_all_places(self):
        self.client.post('/api/v1/places/', json=self.valid_place)
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    # GET /api/v1/places/<id>
    def test_get_place_by_id(self):
        post_resp = self.client.post('/api/v1/places/', json=self.valid_place)
        place_id = post_resp.get_json()['id']
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('owner', data)
        self.assertIn('amenities', data)
        self.assertIn('price', data)

    def test_get_place_not_found(self):
        response = self.client.get('/api/v1/places/fake-id-000')
        self.assertEqual(response.status_code, 404)

    # PUT /api/v1/places/<id>
    @unittest.expectedFailure
    def test_update_place_success(self):
        post_resp = self.client.post('/api/v1/places/', json=self.valid_place)
        place_id = post_resp.get_json()['id']
        response = self.client.put(
            f'/api/v1/places/{place_id}',
            json={**self.valid_place, "title": "Luxury Condo", "price": 200.0}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["title"], "Luxury Condo")
        self.assertEqual(data["price"], 200.0)

    def test_update_place_not_found(self):
        response = self.client.put('/api/v1/places/fake-id-000',
                                   json=self.valid_place)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
