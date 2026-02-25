from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')


# =========================
# API MODELS
# =========================

user_model = api.model('User', {
    'first_name': fields.String(
        required=True,
        description='First name of the user'
    ),
    'last_name': fields.String(
        required=True,
        description='Last name of the user'
    ),
    'email': fields.String(
        required=True,
        description='Email of the user'
    ),
    'password': fields.String(
        required=True,
        description='Password of the user'
    )
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(
        description='First name of the user'
    ),
    'last_name': fields.String(
        description='Last name of the user'
    ),
    'email': fields.String(
        description='Email of the user'
    ),
    'password': fields.String(
        description='New password'
    )
})


# =========================
# USER LIST RESOURCE
# =========================

@api.route('/')
class UserList(Resource):
    """
    Resource for creating and retrieving users.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data or email already registered')
    def post(self):
        """
        Register a new user.

        Expects:
            JSON payload containing first_name, last_name,
            email, and password.

        Returns:
            dict: Created user information (without password).
            HTTP 201 on success.
            HTTP 400 if validation fails or email exists.
        """
        user_data = api.payload

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

    @api.response(200, 'Users list retrieved successfully')
    def get(self):
        """
        Retrieve all registered users.

        Returns:
            list: List of users (without password).
            HTTP 200 on success.
        """
        users = facade.get_all_users()

        return [
            {
                'id': u.id,
                'first_name': u.first_name,
                'last_name': u.last_name,
                'email': u.email
            }
            for u in users
        ], 200


# =========================
# SINGLE USER RESOURCE
# =========================

@api.route('/<user_id>')
class UserResource(Resource):
    """
    Resource for retrieving and updating a specific user.
    """

    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a user by their unique ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            dict: User information (without password).
            HTTP 200 on success.
            HTTP 404 if user does not exist.
        """
        user = facade.get_user(user_id)

        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update an existing user.

        Allows updating first_name, last_name, email,
        and password.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            dict: Updated user information (without password).
            HTTP 200 on success.
            HTTP 404 if user not found.
            HTTP 400 if validation fails.
        """
        try:
            user = facade.update_user(user_id, api.payload)

            if not user:
                return {'error': 'User not found'}, 404

        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
