from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():    
    data = request.get_json()
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}, 201), 

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 400

    access_token = create_access_token(identity={'username': user.username})
    return jsonify({'access_token': access_token}), 200

@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
