import pytest
import requests
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    # Create a Flask app instance with testing configuration
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://greama:Nanochinedu72@localhost/user_auth_db'  # Ensure this matches your PostgreSQL URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for testing

    with app.app_context():
        db.create_all()  # Create all tables
        yield app  # Yield the app for testing
        db.session.remove()  # Clean up the session
        db.drop_all()  # Drop all tables after the tests

def test_login_endpoint_successful(app):
    with app.app_context():
        # Create a test user
        test_user = User(userId='test_user', email='test@example.com', firstName='Test', lastName='User')
        test_user.set_password('test_password')
        db.session.add(test_user)
        db.session.commit()

    url = 'http://localhost:5000/auth/login'
    data = {
        'userId': 'test_user',
        'password': 'test_password'
    }
    
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert 'accessToken' in response.json()['data']
    assert response.json()['data']['user']['userId'] == 'test_user'

def test_login_endpoint_invalid_credentials(app):
    with app.app_context():
        # Create a test user
        test_user = User(userId='test_user', email='test@example.com', firstName='Test', lastName='User')
        test_user.set_password('test_password')
        db.session.add(test_user)
        db.session.commit()

    url = 'http://localhost:5000/auth/login'
    data = {
        'userId': 'test_user',
        'password': 'wrong_password'
    }
    
    response = requests.post(url, json=data)
    assert response.status_code == 401
    assert 'Invalid username or password' in response.json()['message']

def test_login_endpoint_user_not_found(app):
    url = 'http://localhost:5000/auth/login'
    data = {
        'userId': 'non_existing_user',
        'password': 'test_password'
    }
    
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert 'Invalid username or password' in response.json()['message']
