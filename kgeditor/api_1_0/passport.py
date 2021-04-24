from flask_restx import Resource, fields
from . import api
from kgeditor.dao.passport import UserDAO
from flask import abort
import re

ns = api.namespace("User", path="/users", description="User operations")
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

@ns.route("/")
class Users(Resource):
    """Show a list of all graphs, and lets you post to add """
    @ns.doc("register_user")
    @ns.marshal_with(user, code=201)
    @ns.response(400, 'Validation error')
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

        return user_dao.create(api.payload), 201

# @ns.route("/<int:id>")
# @ns.response(404, 'Graph not found')
# @ns.param('id', "The graph identifier")
# class Graph(Resource):
#     """"""