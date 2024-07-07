# routes.py

from flask import Flask, Blueprint, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Organization

main = Blueprint('main', __name__)
app = Flask(__name__)

@app.route('/')
def index():
    if current_app:
        return jsonify(message="Flask is initialized.")
    else:
        return jsonify(message="Flask is not initialized."), 500

@main.route('/api/organisations', methods=['GET'])
@jwt_required()
def get_organisations():
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    organizations = Organization.query.all()
    user_organizations = []
    for org in organizations:
        user_organizations.append({
            'orgId': org.orgId,
            'name': org.name,
            'description': org.description
        })

    return jsonify({
        'status': 'success',
        'message': 'User organisations retrieved successfully',
        'data': {
            'organisations': user_organizations
        }
    }), 200

@main.route('/api/organisations/<orgId>', methods=['GET'])
@jwt_required()
def get_organization(orgId):
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(userId=current_user_id).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

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
