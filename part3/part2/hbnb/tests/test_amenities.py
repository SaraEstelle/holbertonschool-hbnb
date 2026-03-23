import unittest
from app import create_app


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    # POST /api/v1/amenities/
    def test_create_amenity_success(self):
        response = self.client.post('/api/v1/amenities/',
                                    json={"name": "Wi-Fi"})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['name'], 'Wi-Fi')

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_name_too_long(self):
        response = self.client.post('/api/v1/amenities/',
                                    json={"name": "A" * 51})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

    # GET /api/v1/amenities/
    def test_get_all_amenities_empty(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_all_amenities(self):
        self.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    # GET /api/v1/amenities/<id>
    def test_get_amenity_by_id(self):
        post_resp = self.client.post('/api/v1/amenities/',
                                     json={"name": "Wi-Fi"})
        amenity_id = post_resp.get_json()['id']
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/fake-id-000')
        self.assertEqual(response.status_code, 404)

    # PUT /api/v1/amenities/<id>
    def test_update_amenity_success(self):
        post_resp = self.client.post('/api/v1/amenities/',
                                     json={"name": "Wi-Fi"})
        amenity_id = post_resp.get_json()['id']
        response = self.client.put(
            f'/api/v1/amenities/{amenity_id}',
            json={"name": "Air Conditioning"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.get_json())

    def test_update_amenity_not_found(self):
        response = self.client.put('/api/v1/amenities/fake-id-000',
                                   json={"name": "Air Conditioning"})
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
