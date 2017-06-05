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
                    }, 409
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
    def items():
        def post(self, id):
        #create a new bucketlist item
        bucketlist_item = request.get_json()
        if not bucketlist_item:
            response = jsonify({'Error': 'No data provided', 'status': 400})
            return response
        item_name = bucketlist_item['name']
        bucketlist = BucketListItems.query.filter_by(bucketlist_id=id).all()
        if bucketlist:
            for item in bucketlist:
                print(item)
                if item.name == item_name:
                    response = jsonify({'Error':'Item already exists', 'status': 409})
                    return response

        #add item
        item=BucketListItems(name=item_name, bucketlist_id=id)
        item.add(item)
        return jsonify({'Message':'Successfully added item', 'status': 201})

    @app.route('/api/v1.0/bucketlists/<int:id>/items/', methods=['PUT','DELETE'])
    def items_manipulation():
        def get(self, id, item_id):
        #get a specific item for a particular bucketlist
        if BucketListItems.query.filter_by(bucketlist_id=id) and BucketListItems.query.filter_by(id=item_id):
            items = BucketListItems.query.get(item_id)
            print(items)
            if items:
                return bucket_list_item_schema.dump(items)
            else:
                response = jsonify({'Error': 'Item not found','status': 404})
                return response
    def put(self, id, item_id):
        #update a particular item for a specific bucketlist
        user = g.user.user_id
        bucketlist_creator = BucketList.query.filter_by(created_by=user).filter_by(id=id)
        if bucketlist_creator:
            item = BucketListItems.query.filter_by(bucketlist_id=id).filter_by(id=item_id).first()
            if item:
                item_data = request.get_json()
                print(item_data)
                errors = bucket_list_schema.validate(item_data)
                if errors:
                    return jsonify({'error':'Check your fields and try again', 'status': 400})
                if 'done' in item_data:
                    done = item_data['done']
                    item.done = done
                new_name = item_data['name']
                item.name = new_name
                item.update()
                return jsonify({'message':'Successfully updated','status': 200})
            return jsonify({'error':'Item not found','status': 400})
        return jsonify({'error':'Unauthorized access','status': 401})
    def delete(self, id, item_id):
        user = g.user.user_id
        bucketlist_creator = BucketList.query.filter_by(created_by=user)
        if bucketlist_creator:
            item = BucketListItems.query.filter_by(bucketlist_id=id).filter_by(id=item_id).first()
            if item:
                item.delete(item)
                return jsonify({'message':'Successfully deleted item','status': 200})

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
