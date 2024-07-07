import unittest
import json
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        response = self.client.post('/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully', data['message'])

        # Verify user is in the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'testuser@example.com')

    def test_login(self):
        self.client.post('/auth/register', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })

        response = self.client.post('/auth/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_invalid_login(self):
        response = self.client.post('/auth/login', json={
            'username': 'nonexistentuser',
            'password': 'wrongpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', data['message'])

if __name__ == '__main__':
    unittest.main()
