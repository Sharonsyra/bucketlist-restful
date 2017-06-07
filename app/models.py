import re
from app import db
from flask_bcrypt import Bcrypt
from flask import current_app
import jwt
from datetime import datetime, timedelta


class User(db.Model):
    """user table class """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship(
        'Bucketlist', order_by='Bucketlist.id', cascade="all, delete-orphan")

    def __init__(self, email, password):
        """User credentials."""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def password_is_valid(self, password):
        """Validate user password"""
        return Bcrypt().check_password_hash(self.password, password)

    def save(self):
        """Register and save user"""
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generate Authorization header token"""

        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=20),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token given the authorization token."""
        try:
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token. Please log in to get a new token"
        except jwt.InvalidTokenError:
            return "Invalid token. Please register or login"


class Bucketlist(db.Model):
    """Bucketlist table class"""
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False) 
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship('Item', order_by='Item.id',
                            cascade="all, delete-orphan")

    def __init__(self, name, created_by):
        """Bucketlist constructor with name and creator."""
        self.name = name
        self.created_by = created_by

    def save(self):
        """Save bucketlist data to db"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        """Get all bucketlists of a user."""
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        """Deletes a bucketlist."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Bucketlist object representation."""
        return "<Bucketlist {}>".format(self.title)

class Item(db.Model):
    """Item table class"""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))

    def __init__(self, name, bucketlist_id):
        """Item with name and bucket list."""
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        """save item data"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        """This method gets all the items in a given bucketlist."""
        return Item.query.filter_by(bucketlist_id=bucketlist_id)

    def delete(self):
        """Deletes an item."""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """Item object representation."""
        return "<Item {}>".format(self.name)
