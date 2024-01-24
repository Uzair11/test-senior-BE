import time
from flask import Blueprint, jsonify, request, abort
from flasgger.utils import swag_from
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity
)
from app.models import db
from app.models.user_model import User
from app.serializers.base import BaseUserSerializer


authRoute = Blueprint('authRoute', __name__)

@swag_from('../api_docs/register_user.yml')
@authRoute.route('/register', methods=['POST'])
def register_user():
    try:
        user = dict(request.get_json())
        user_schema = BaseUserSerializer(many=False)
        validated_data = user_schema.load(user, session=db.session)
        db.session.add(validated_data)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except SQLAlchemyError as err:
        return jsonify({"errors": err}), 400
    except Exception as err:
        return jsonify({"errors": err}), 400

@swag_from('../api_docs/login_user.yml')
@authRoute.route('/login', methods=['POST'])
def login_user():
    try:
        login_creds = dict(request.get_json())
        user = User.query.filter_by(email=login_creds['email']).first()
        if not user:
            return jsonify({"errors": "User not found"}), 400
        if not user.password == login_creds['password']:
            return jsonify({"errors": "Incorrect password"}), 400
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    except SQLAlchemyError as err:
        return jsonify({"errors": err}), 400
    except Exception as err:
        return jsonify({"errors": err}), 400

@authRoute.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    try:
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify({"access_token": access_token}), 200
    except Exception as err:
        return jsonify({"errors": err}), 400
    
    