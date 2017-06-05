import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """Bucketlist Test Case"""
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go bungee jumping!'}

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

        self.assertEqual(response_by_id.status_code, 200)
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
            headers=dict(Authorization="Bearer " + access_token),)
        self.assertEqual(response.status_code, 409)
        result = self.client().get(
            '/api/v1.0/bucketlists/1',
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(result.status_code, 404)

    def test_bucketlist_item_creation(self):
        pass

    def test_bucketlist_item_creation_duplicates(self):
        pass

    def test_bucketlist_view_items(self):
        pass

    def test_bucketlist_view_item(self):
        pass

    def test_bucketlist_item_edit(self):
        pass

    def test_bucketlist_item_deletion(self):
        pass

if __name__ == "__main__":
    unittest.main()
