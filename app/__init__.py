import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

from config import app_config

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app(config_name):

    from app.models import Bucketlist, User

    app = FlaskAPI(__name__, instance_relative_config=True)
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1.0/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                if request.method == "POST":
                    bucketlist = Bucketlist.query.filter_by(name=request.data['name']).first()
                    if not bucketlist:
                        name = str(request.data.get('name', ''))
                        if name:
                            bucketlist = Bucketlist(name=name, created_by=user_id)
                            bucketlist.save()
                            response = jsonify({
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'created_by': user_id
                            })

                            return make_response(response), 201
                    else:
                        response = {
                        'message': 'Bucketlist name already exists!'
                         }
                        return make_response(jsonify(response)), 409

                elif request.method == "GET":
                    bucketlists = Bucketlist.get_all(user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
                else:
                    message = user_id
                    response = {
                    "message":message
                    }
                    return make_response(jsonify(response)), 400

        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401

    @app.route('/api/v1.0/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):

        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    abort(404)

                if request.method == "DELETE":
                    bucketlist.delete()
                    return {
                        "message": "bucketlist {} deleted".format(bucketlist.id)
                    }, 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    bucketlist.name = name
                    bucketlist.save()
                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200
                else:
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    })
                    return make_response(response), 200
            else:
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401

    @app.route('/api/v1.0/bucketlists/<int:id>/items/', methods=['POST','GET'])
    def items(id, **kwargs):
        pass
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(name=request.data['name']).first()
                if bucketlist:
                    if request.method == "POST":
                        item = Item.query.filter_by(name=request.data['name']).first()
                        if not item:
                            name = str(request.data.get('name', ''))
                            if name:
                                item = Item(name=name, list_id=bucketlist_id)
                                item.save()
                                response = jsonify({
                                    'id':item.id,
                                    'name':item.name,
                                    'done':item.done,
                                    'date_created':item.date_created,
                                    'date_modified':item.date_modified,
                                    'list_id':bucketlist_id
                                })
                                return make_response(response), 201
                        else:
                            response = {
                            'message': 'Item name already exists!'
                             }
                            return make_response(jsonify(response)), 409
                    elif request.method == "GET":
                        items = Item.get_all(bucketlist_id)
                        results = []

                        for item in items:
                            obj = {
                                'id':item.id,
                                'name':item.name,
                                'done':item.done,
                                'date_created':item.date_created,
                                'date_modified':item.date_modified,
                                'list_id':item.list_id
                            }
                            results.append(obj)
                        return make_response(jsonify(results)), 200

                    else:
                        message = user_id
                        response = {
                        "message":message
                        }
                        return make_response(jsonify(response)), 400

                elif not bucketlist:
                    response = {
                        'message': 'The bucketlist does not exist!'
                         }
                    return make_response(jsonify(response)), 404
        else:
            message = user_id
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 401


    @app.route('/api/v1.0/bucketlists/<int:id>/items/', methods=['PUT','DELETE'])
    def items_manipulation():
        pass

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
