"""
User API module.

This module defines the RESTful endpoints for managing User objects
in the Hbnb application. The PUT endpoint is protected by JWT authentication.

Access rules:
- POST /     : Admin only (create user)
- GET /      : Public
- GET /<id>  : Public
- PUT /<id>  : Authenticated user (own data only, no email/password)
               OR Admin (any user, email and password allowed)
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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
    ),
    'is_admin': fields.Boolean(
        description='Whether the user has admin privileges',
        default=False
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
    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(422, 'Email already registered')
    def post(self):
        """
        Register a new user.Public endpoint.

        Expects:
            JSON payload containing first_name, last_name,
            email, and password.

        Returns:
            dict: Created user information (without password).
            HTTP 201 on success.
            HTTP 400 if validation fails.
            HTTP 422 if email already exists.
        """
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload

        try:
            new_user = facade.create_user(user_data)
        except ValueError as e:
            if "Email already exists" in str(e):
                return {'error': str(e)}, 422
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

    @jwt_required()
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Cannot modifiy email or password')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update user details.
        - Regular user : Can only modifiy their own first_name / last_name.
        Email and passwird are blocked.
        - Admin: can modify any user including email and password.
        Email must remain unique.
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        data = api.payload

        if is_admin:
            # Admin can modify any user including email and password
            email = data.get('email')
            if email:
                existing = facade.get_user_by_email(email)
                if existing and existing.id != user_id:
                    return {'error': 'Email already in use'}, 400

            try:
                user = facade.update_user(user_id, data)
                if not user:
                    return {'error': 'User not found'}, 404
            except ValueError as e:
                return {'error': str(e)}, 400

        else:
            # Regular user : can only modifiy their own data
            if user_id != current_user_id:
                return {'error': 'Unauthorized action'}, 403

            #Email and password are forbidden
            if 'email' in data or 'password' in data:
                return {'error': 'You cannot modify email or password'}, 400

            try:
                user = facade.update_user(user_id, data)
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

    @jwt_required()
    @api.response(200, 'User successfully deleted')
    @api.response(400, 'Cannot delete your own account')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    def delete(self, user_id):
        """Delete a user. Admin only. Cannot delete yourself."""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        current_user_id = get_jwt_identity()
        if user_id == current_user_id:
            return {'error': 'Cannot delete your own admin account'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        facade.delete_user(user_id)
        return {'message': 'User successfully deleted'}, 200

