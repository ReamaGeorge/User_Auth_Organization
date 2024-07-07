#app/auth.py

import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_wtf.csrf import generate_csrf
from .models import db, User, Organization
from .forms import RegistrationForm, LoginForm

auth = Blueprint('auth', __name__)

# Route to get CSRF token
@auth.route('/csrf_token', methods=['GET'])
def get_csrf_token():
    csrf_token = generate_csrf()
    return jsonify({'csrf_token': csrf_token}), 200

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Registration endpoint
@auth.route('/register', methods=['POST'])
# @csrf.exempt
def register():
    data = request.get_json()
    form = RegistrationForm(data=data)
  
    if form.validate_on_submit():
        userId = form.userId.data
        email = form.email.data
        password = form.password.data
        organization_name = form.organization_name.data
        organization_description = form.organization_description.data
  
        # Check if username or email already exists
        existing_user = User.query.filter((User.userId == userId) | (User.email == email)).first()
        if existing_user:
            return jsonify({'message': 'User already exists'}), 400

        # Create new organization if it doesn't exist
        existing_organization = Organization.query.filter_by(name=organization_name).first()
        if not existing_organization:
            new_organization = Organization(name=organization_name, description=organization_description)
            db.session.add(new_organization)
            db.session.commit()
            organization_id = new_organization.id
        else:
            organization_id = existing_organization.id

        # Create new user and hash password
        new_user = User(userId=userId, email=email, firstName=form.firstName.data, lastName=form.lastName.data, phone=form.phone.data)
        new_user.set_password(password)
        new_user.organizations.append(Organization.query.get(organization_id))
        db.session.add(new_user)
        db.session.commit()
  
        # Generate access token
        access_token = create_access_token(identity=userId)
  
        return jsonify({
            'status': 'success',
            'message': 'Registration successful',
            'data': {
                'accessToken': access_token,
                'user': {
                    'userId': new_user.userId,
                    'firstName': new_user.firstName,
                    'lastName': new_user.lastName,
                    'email': new_user.email,
                    'phone': new_user.phone
                },
                'organization': {
                    'name': organization_name,
                    'description': organization_description
                }
            }
        }), 201
    else:
        return jsonify({'errors': form.errors}), 422

# Login endpoint
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    form = LoginForm(data=data)
  
    if form.validate_on_submit():
        userId = form.userId.data
        password = form.password.data
  
        # Verify user credentials
        user = User.query.filter_by(userId=userId).first()
        if not user or not user.check_password(password):
            return jsonify({'message': 'Invalid username or password'}), 401
  
        # Generate access token
        access_token = create_access_token(identity=userId)
  
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'accessToken': access_token,
                'user': {
                    'userId': user.userId,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'phone': user.phone
                }
            }
        }), 200
    else:
        return jsonify({'errors': form.errors}), 422

# User details endpoint
@auth.route('/api/users/<id>', methods=['GET', 'PUT'])
@jwt_required()
def user_details(id):
    current_user_id = get_jwt_identity()
    if current_user_id != id:
        return jsonify({'message': 'Unauthorized'}), 401

    user = User.query.filter_by(userId=id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify({
            'status': 'success',
            'message': 'User details retrieved successfully',
            'data': {
                'userId': user.userId,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'phone': user.phone
            }
        }), 200

    elif request.method == 'PUT':
        data = request.get_json()
        user.firstName = data.get('firstName', user.firstName)
        user.lastName = data.get('lastName', user.lastName)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'User details updated successfully',
            'data': {
                'userId': user.userId,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'phone': user.phone
            }
        }), 200

# Organizations endpoints
@auth.route('/api/organisations', methods=['GET', 'POST'])
@jwt_required()
def organizations():
    if request.method == 'GET':
        organizations = Organization.query.all()
        org_list = [{
            'orgId': org.orgId,
            'name': org.name,
            'description': org.description
        } for org in organizations]

        return jsonify({
            'status': 'success',
            'message': 'Organizations retrieved successfully',
            'data': {
                'organizations': org_list
            }
        }), 200

    elif request.method == 'POST':
        data = request.get_json()
        orgId = data.get('orgId')
        name = data.get('name')
        description = data.get('description')

        existing_org = Organization.query.filter_by(orgId=orgId).first()
        if existing_org:
            return jsonify({'message': 'Organization already exists'}), 400

        new_org = Organization(orgId=orgId, name=name, description=description)
        db.session.add(new_org)
        db.session.commit()

        return jsonify({
            'status': 'success',
            'message': 'Organization created successfully',
            'data': {
                'orgId': new_org.orgId,
                'name': new_org.name,
                'description': new_org.description
            }
        }), 201

# Organization details endpoint
@auth.route('/api/organisations/<orgId>', methods=['GET'])
@jwt_required()
def organization_details(orgId):
    organization = Organization.query.filter_by(orgId=orgId).first()
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404

    return jsonify({
        'status': 'success',
        'message': 'Organization retrieved successfully',
        'data': {
            'orgId': organization.orgId,
            'name': organization.name,
            'description': organization.description
        }
    }), 200

# Users in organization endpoint
@auth.route('/api/organisations/<orgId>/users', methods=['GET'])
@jwt_required()
def organization_users(orgId):
    organization = Organization.query.filter_by(orgId=orgId).first()
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404

    users = organization.users.all()
    user_list = [{
        'userId': user.userId,
        'firstName': user.firstName,
        'lastName': user.lastName,
        'email': user.email,
        'phone': user.phone
    } for user in users]

    return jsonify({
        'status': 'success',
        'message': 'Users in organization retrieved successfully',
        'data': {
            'organization': {
                'orgId': organization.orgId,
                'name': organization.name,
                'description': organization.description
            },
            'users': user_list
        }
    }), 200

# Add user to organization endpoint
@auth.route('/api/organisations/<orgId>/users', methods=['POST'])
@jwt_required()
def add_user_to_organization(orgId):
    data = request.get_json()
    userId = data.get('userId')

    organization = Organization.query.filter_by(orgId=orgId).first()
    if not organization:
        return jsonify({'message': 'Organization not found'}), 404

    user = User.query.filter_by(userId=userId).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if user not in organization.users:
        organization.users.append(user)
        db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'User added to organization successfully'
    }), 200
