import sys
import unittest
import json

from os import path
from app import create_app, db

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class BucketlistTestCase(unittest.TestCase):
    """Bucketlist Test Case"""

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go bungee jumping!'}
        self.item = {'name': 'Buy gym wear!'}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        """Sample registration data"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1.0/auth/register', data=user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        """Sample login data"""
        user_data = {
            'email': email,
            'password': password
        }
        return self.client().post('/api/v1.0/auth/login', data=user_data)

    def test_bucketlist_creation(self):
        """Test that bucketlist is created"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go bungee', str(response.data))

    def test_bucketlist_creation_duplicates(self):
        """Test user cannot create duplicate bucketlists"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go bungee', str(response.data))
        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 409)

    def test_bucketlist_view_all(self):
        """Test that all bucketlists are viewed"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        response = self.client().get(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Go bungee', str(response.data))

    def test_bucketlist_view_one(self):
        """Test one bucketlist can be viewed"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())
        result = self.client().get(
            '/api/v1.0/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go bungee', str(result.data))

    def test_bucketlist_edit(self):
        """Test that a bucketlist can be edited"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go sky-diving'})
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())
        response_by_id = self.client().put(
            '/api/v1.0/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={
                "name": "Go sky-diving at Diani)"
            })

        self.assertEqual(response_by_id.status_code, 201)
        results = self.client().get(
            '/api/v1.0/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertIn('Go sky-diving', str(results.data))

    def test_bucketlist_deletion(self):
        """Test that a bucketlist can be deleted"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Go sky-diving'})
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())
        response = self.client().delete(
            '/api/v1.0/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(response.status_code, 200)
        result = self.client().get(
            '/api/v1.0/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_bucketlist_item_creation(self):
        """Test that bucketlist can create an item"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        self.assertIn('Buy gym', str(item_response.data))

    def test_bucketlist_item_creation_no_bucketlist(self):
        """Test that item cannot be created without an existing bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().get(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(response_by_id.status_code, 200)
        item_response = self.client().post(
            '/api/v1.0/bucketlists/1/items/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 404)
        self.assertIn('The bucketlist does not exist!',
                      str(item_response.data))

    def test_bucketlist_item_creation_duplicates(self):
        """Test that bucketlist cannot have duplicate items"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        self.assertIn('Buy gym', str(item_response.data))
        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 409)

    def test_bucketlist_view_items(self):
        """Test that bucketlist items can be viewed"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        self.assertIn('Buy gym', str(item_response.data))
        item_response = self.client().get(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(item_response.status_code, 200)

    def test_bucketlist_view_item(self):
        """Test that one can view a single bucket list item"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        item_result = json.loads(item_response.data.decode())
        item_response = self.client().get(
            '/api/v1.0/bucketlists/{}/items/{}'.format(results['id'],
                                                       item_result['id']),
            headers=dict(Authorization="Bearer " + access_token)
        )
        self.assertEqual(item_response.status_code, 200)
        self.assertIn('Buy gym', str(item_response.data))

    def test_bucketlist_item_edit(self):
        """Test that a bucketlist item can be edited"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())
        result = self.client().get(
            '/api/v1.0/bucketlists/{}'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go bungee', str(result.data))

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        self.assertIn('gym wear', str(item_response.data))

        item_result = json.loads(item_response.data.decode())

        item_response = self.client().put(
            '/api/v1.0/bucketlists/{}/items/{}'.format(results['id'],
                                                       item_result['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data={'name': 'Buy a travel bag'})
        self.assertEqual(item_response.status_code, 200)
        self.assertIn('travel bag', str(item_response.data))

        results = self.client().get(
            '/api/v1.0/bucketlists/{}/items/{}'.format(results['id'],
                                                       item_result['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(results.status_code, 200)
        self.assertIn('travel bag', str(results.data))

    def test_bucketlist_item_deletion(self):
        """Test that bucketlist item can be deleted"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        results = json.loads(response_by_id.data.decode())

        item_response = self.client().post(
            '/api/v1.0/bucketlists/{}/items/'.format(results['id']),
            headers=dict(Authorization="Bearer " + access_token),
            data=self.item)
        self.assertEqual(item_response.status_code, 201)
        self.assertIn('Buy gym', str(item_response.data))
        item_result = json.loads(item_response.data.decode())

        item_response = self.client().delete(
            '/api/v1.0/bucketlists/1/items/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(item_response.status_code, 200)

        result = self.client().get(
            '/api/v1.0/bucketlists/{}/items/{}'.format(results['id'],
                                                       item_result['id']),
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_pagination_default_limit(self):
        """Test that pagination returns the limit specified"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go bungee', str(response.data))

        result = self.client().get(
            '/api/v1.0/bucketlists?page=1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)

    def test_pagination_set_limit(self):
        """Test that pagination returns the limit specified"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go bungee', str(response.data))

        result = self.client().get(
            '/api/v1.0/bucketlists?page=1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)

    def test_search_name(self):
        """Test that search for a bucketlist"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        result = self.client().get(
            '/api/v1.0/bucketlists?q=bungee',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 200)

    def test_search_non_existent(self):
        """Test that search recognizes a non existent search"""
        self.register_user()
        result = self.login_user()
        access_token = json.loads(result.data.decode())['access_token']

        response_by_id = self.client().post(
            '/api/v1.0/bucketlists/',
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        self.assertEqual(response_by_id.status_code, 201)
        result = self.client().get(
            '/api/v1.0/bucketlists?q=computer',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
