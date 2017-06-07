import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

from config import app_config

from flask_bcrypt import Bcrypt

db = SQLAlchemy()

def create_app(config_name):

    from app.models import User, Bucketlist, Item

    app = FlaskAPI(__name__, instance_relative_config=True)
    bcrypt = Bcrypt(app)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/api/v1.0/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if not auth_header:
            response = {
                "message": "Unauthorised Access"
            }
            return make_response(jsonify(response)), 401


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
                                'items':bucketlist.items,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'created_by': user_id
                            })

                            return make_response(response), 201
                        else:
                            response = {
                                "message": "Please input name!"
                            }
                            return make_response(jsonify(response))

                    else:
                        response = {
                        'message': 'Bucketlist name already exists!'
                         }
                        return make_response(jsonify(response)), 409

                elif request.method == "GET":
                    search = request.args.get("q","")
                    if not search:
                        if request.args.get("page"):
                            page = int(request.args.get("page"))
                        else:
                            page = 1
                        if request.args.get("limit") and int(request.args.get("limit")) < 100:
                            limit = int(request.args.get("limit"))
                        else:
                            limit = 2
                        paginated_buckets = Bucketlist.query.filter_by(
                            created_by=user_id).paginate(page, limit, False)
                        bucketlists = paginated_buckets.items
                        if paginated_buckets.has_next:
                            nextpage = '/bucketlist/api/v1.0/bucketlists/?page=' + \
                                str(page + 1) + '&limit=' + str(limit)
                        else:
                            nextpage = "Nothing To See Here"
                        if paginated_buckets.has_prev:
                            previouspage = '/bucketlist/api/v1.0/bucketlists/?page=' + \
                                str(page - 1) + '&limit=' + str(limit)
                        else:
                            previouspage = "Nothing To See Here"
                        results = []
                        # search all bucketlists
                        for bucketlist in bucketlists:
                            obj = {
                                'id': bucketlist.id,
                                'name': bucketlist.name,
                                'items':bucketlist.items,
                                'date_created': bucketlist.date_created,
                                'date_modified': bucketlist.date_modified,
                                'created_by': bucketlist.created_by
                            }
                            results.append(obj)
                            response = {
                            "next page": nextpage,
                            "previous page": previouspage,
                            "bucketlists": results
                            }
                            return make_response(jsonify(response)), 200

                    if search:
                        search_name = Bucketlist.query.filter_by(Bucketlist.name.ilike(search)).all
                        if not search_name:
                            response = {
                            "message": "Bucketlist does not exist!"
                            }
                            return make_response(jsonify(response)), 404
                        else:
                            bucketlist = Bucketlist.query.filter_by(name=search_name).first()
                            response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'items':bucketlist.items,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                            })
                            return make_response(response), 200

                    # bucketlists = Bucketlist.get_all(user_id)

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

        if not auth_header:
            response = {
                "message": "Unauthorised Access"
            }
            return make_response(jsonify(response)), 401

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if not bucketlist:
                    abort(404)
                elif request.method == "GET":
                    response = jsonify({
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items':bucketlist.items,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    })
                    return make_response(response), 200
                elif request.method == 'PUT':
                    name = str(request.data.get('name', ''))
                    bucketlist.name = name
                    bucketlist.save()
                    response = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'items':bucketlist.items,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        'created_by': bucketlist.created_by
                    }
                    return make_response(jsonify(response)), 200
                elif request.method == "DELETE":
                    bucketlist.delete()
                    return {
                        "message": "bucketlist {} deleted".format(bucketlist.id)
                    }, 200
                
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

    @app.route('/api/v1.0/bucketlists/<int:id>/items/', methods=['POST','GET'])
    def items(id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if not auth_header:
            response = {
                "message": "Unauthorised Access"
            }
            return make_response(jsonify(response)), 401

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if bucketlist:
                    if request.method == "POST":
                        item = Item.query.filter_by(name=request.data['name']).first()
                        if not item:
                            name = str(request.data.get('name', ''))
                            if name:
                                item = Item(name=name, bucketlist_id=id)
                                item.save()
                                response = jsonify({
                                    'id':item.id,
                                    'name':item.name,
                                    'done':item.done,
                                    'date_created':item.date_created,
                                    'date_modified':item.date_modified,
                                    'bucketlist_id':id
                                })
                                return make_response(response), 201
                            else:
                                response = {
                                "message": "Please input name!"
                                 }
                                return make_response(jsonify(response))
                        else:
                            response = {
                            'message': 'Item name already exists!'
                             }
                            return make_response(jsonify(response)), 409
                    elif request.method == "GET":
                        items = Item.get_all(id)
                        results = []
                        if items:
                            for item in items:
                                obj = {
                                    'id':item.id,
                                    'name':item.name,
                                    'done':item.done,
                                    'date_created':item.date_created,
                                    'date_modified':item.date_modified,
                                    'bucketlist_id':id
                                }
                                results.append(obj)
                            return make_response(jsonify(results)), 200
                        else:
                            abort(404)
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

    @app.route('/api/v1.0/bucketlists/<int:id>/items/<int:item_id>', methods=['GET','PUT', 'DELETE'])
    def items_manipulation(id, **kwargs):
        auth_header = request.headers.get('Authorization')
        access_token = auth_header.split(" ")[1]

        if not auth_header:
            response = {
                "message": "Unauthorised Access"
            }
            return make_response(jsonify(response)), 401

        if access_token:
            user_id = User.decode_token(access_token)
            if not isinstance(user_id, str):
                bucketlist = Bucketlist.query.filter_by(id=id).first()
                if bucketlist:
                    item = Item.query.filter_by(id=id).first()
                    if item:
                        if request.method == "GET":
                            response = jsonify({
                            'item_id': item.id,
                            'name': item.name,
                            'done': item.done,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'bucketlist_id':id
                            })
                            return make_response(response), 200

                        elif request.method == "PUT":
                            name = str(request.data.get('name', ''))
                            done = bool(request.data.get('done',))
                            item.name = name
                            item.save()
                            response = {
                                'item_id': item.id,
                                'name': item.name,
                                'done':item.done,
                                'date_created': item.date_created,
                                'date_modified': item.date_modified,
                                'bucketlist_id':id
                            }
                            return make_response(jsonify(response)), 200

                        elif request.method == "DELETE":
                            item.delete()
                            return {
                            "message": "Item {} deleted".format(item.id)
                            }, 200
                        else:
                            message = user_id
                            response = {
                            "message":message
                            }
                            return make_response(jsonify(response)), 400
                    else:
                        response = {
                        'message': 'The item does not exist!'
                         }
                        return make_response(jsonify(response)), 404                     
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


    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
