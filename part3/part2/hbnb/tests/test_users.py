import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True
        self.valid_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "secret12"
        }

    # POST /api/v1/users/
    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json=self.valid_user)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertNotIn('password', data)

    def test_create_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json=self.valid_user)
        response = self.client.post('/api/v1/users/', json=self.valid_user)
        self.assertEqual(response.status_code, 422)

    def test_create_user_invalid_email(self):
        payload = {**self.valid_user, "email": "not-an-email"}
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_user_empty_first_name(self):
        payload = {**self.valid_user, "first_name": ""}
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_user_name_too_long(self):
        payload = {**self.valid_user, "first_name": "A" * 51}
        response = self.client.post('/api/v1/users/', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_field(self):
        response = self.client.post('/api/v1/users/',
                                    json={"first_name": "Jane"})
        self.assertEqual(response.status_code, 400)

    # GET /api/v1/users/
    def test_get_all_users_empty(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_get_all_users(self):
        self.client.post('/api/v1/users/', json=self.valid_user)
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

    # GET /api/v1/users/<id>
    def test_get_user_by_id_success(self):
        post_resp = self.client.post('/api/v1/users/', json=self.valid_user)
        user_id = post_resp.get_json()['id']
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.get_json())

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/fake-id-000')
        self.assertEqual(response.status_code, 404)

    # PUT /api/v1/users/<id>
    def test_update_user_success(self):
        post_resp = self.client.post('/api/v1/users/', json=self.valid_user)
        user_id = post_resp.get_json()['id']
        response = self.client.put(
            f'/api/v1/users/{user_id}',
            json={"first_name": "Jane"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['first_name'], 'Jane')

    def test_update_user_not_found(self):
        response = self.client.put('/api/v1/users/fake-id-000',
                                   json={"first_name": "Jane"})
        self.assertEqual(response.status_code, 404)

    def test_update_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json=self.valid_user)
        r2 = self.client.post('/api/v1/users/',
                              json={**self.valid_user,
                                    "email": "other@example.com"})
        user2_id = r2.get_json()['id']
        response = self.client.put(
            f'/api/v1/users/{user2_id}',
            json={"email": "john.doe@example.com"}
        )
        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main()
