import re
from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User


class RegistrationView(MethodView):
    """Registers a new user to the api"""
    def post(self):
        user = User.query.filter_by(email=request.data['email']).first()

        post_data = request.data

        match=re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[com|org|edu]{3}$)", 
                        post_data['email'])

        if not post_data['email']:
            response = jsonify({
                "message": "Please enter an email"
            })
            return make_response(response), 400

        if not match:
            response = jsonify({
                "message": "Use the correct email format"
            })
            return make_response(response), 400

        if len(post_data['password']) < 6:
            response = jsonify({
                "message":
                "The length of the password should be at least six characters"
            })
            return make_response(response), 400

        if not user:
            try:
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()

                response = {
                    'message': 'You registered successfully. Login.',
                }
                return make_response(jsonify(response)), 201

            except Exception as e:
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'message': 'User already exists. Login.'
            }

            return make_response(jsonify(response)), 409


class LoginView(MethodView):
    """Logs in a user to the system"""
    def post(self):
        try:
            user = User.query.filter_by(email=request.data['email']).first()

            if user and user.password_is_valid(request.data['password']):
                access_token = user.generate_token(user.id)
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'message': 'Invalid email or password, Please try again.'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:
            response = {
                'message': str(e)
            }
            return make_response(jsonify(response)), 500


registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

auth_blueprint.add_url_rule(
    '/api/v1.0/auth/register',
    view_func=registration_view,
    methods=['POST'])
auth_blueprint.add_url_rule(
    '/api/v1.0/auth/login',
    view_func=login_view,
    methods=['POST']
)
