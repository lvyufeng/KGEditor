from flask_restx import Resource, fields
from . import api
from kgeditor.dao.passport import UserDAO
from flask import abort, session, request
import re
import logging

ns = api.namespace("User", path="/", description="User operations")
user = api.model(
    "User",
    {
        "id": fields.Integer(readonly=True, description='The user unique identifiers'),
        "mobile": fields.String(required=True, example='13712345678', pattern=r'1[34578]\d{9}'),
        "name": fields.String(required=True, example="test_name"),
        "password": fields.String(required=True, example="test_password"),
        "password2": fields.String(required=True, example='test_password')
    }
)
user_dao = UserDAO()

@ns.route("/users")
class Users(Resource):
    """Create a new user"""
    @ns.doc("register_user")
    @ns.response(201, 'Create succeed.')
    @ns.response(400, 'Validation error.')
    @ns.expect(user)
    def post(self):
        """Register a user"""
        req_dict = api.payload
        mobile = req_dict.get('mobile')
        name = req_dict.get('name')
        password = req_dict.get('password')
        password2 = req_dict.get('password2')
        # verify
        if not all([mobile, password, name]):
            return abort(400, "Invalid parameters.")

        # phone number format
        if not re.match(r'1[34578]\d{9}', mobile):
            # wrong format
            return abort(400, "Wrong phone number format.")

        if password != password2:
            return abort(400, "Password validation error.")

        return user_dao.create(api.payload)

@ns.route("/session")
class Session(Resource):
    """User session for login and logout"""
    @ns.doc('get_session')
    @ns.response(200, 'User name.')
    @ns.response(401, 'User not authorized.')
    def get(self):
        name = session.get('name')
        if name is not None:
            return {'name': name}, 200
        return abort(401, 'User should login')

    def post(self):
        """Login"""
        req_dict = api.payload
        mobile = req_dict.get('mobile')
        password = req_dict.get('password')

        # verify parameter
        if not all([mobile, password]):
            return abort(400, 'Invalid parameters.') 

        # phone number format
        if not re.match(r'1[34578]\d{9}', mobile):
            # wrong format
            return abort(400, "Wrong phone number format.")
        # error times
        return user_dao.get(api.payload)

    @ns.doc("user_logout")
    @ns.response(200, 'Logout succeed.')
    def delete(self):
        """User logout"""
        session.clear()
        return {'message': "Logout succeed."}, 200

# @ns.route("/<int:id>")
# @ns.response(404, 'Graph not found')
# @ns.param('id', "The graph identifier")
# class Graph(Resource):
#     """"""