import asyncio

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.lib.connection_utils import prepare_creds
from app.lib.queries_manager import fetch_db_info_postgres, fetch_db_info_mysql, fetch_table_exists_postgres, \
    fetch_table_exists_mysql
from app.models import db
from app.models.db_creds import DBCredentials
from app.serializers.base import BaseDBCredsSchema

dbRoute = Blueprint('dbRoute', __name__)


@dbRoute.route('/submit-creds', methods=['POST'])
@jwt_required()
def submit_db_creds():
    try:
        user = get_current_user()
        db_creds = dict(request.get_json())
        db_creds_schema = BaseDBCredsSchema(many=False)
        validated_data = db_creds_schema.load({**db_creds, 'user_id': user.id},session=db.session)
        db.session.add(validated_data)
        db.session.commit()
        return jsonify({"message": "DB Credentials added successfully"}), 201
    except SQLAlchemyError as err:
        return jsonify({"errors": err}), 400
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


@dbRoute.route('/get-db-info', methods=['GET'])
@jwt_required()
def get_db_info():
    user = get_current_user()
    db_creds_id = request.args.get('db_creds_id', None, type=int)

    if not db_creds_id:
        return jsonify({"errors": "db_creds_id is required"}), 400

    db_creds = DBCredentials.query.filter_by(id=db_creds_id, user_id=user.id).first()
    if not db_creds:
        return jsonify({"errors": "db_creds_id is invalid"}), 400

    db_creds_schema = BaseDBCredsSchema(many=False)
    validated_data = db_creds_schema.dump(db_creds)
    validated_creds = prepare_creds(validated_data)

    db_type = validated_creds.pop('db_type', None)
    fetch_function = None

    if db_type == 'postgresql':
        fetch_function = fetch_db_info_postgres
    elif db_type == 'mysql':
        fetch_function = fetch_db_info_mysql

    if fetch_function:
        db_info = asyncio.run(fetch_function(validated_creds))
        return jsonify(db_info), 200
    else:
        return jsonify({"errors": "Unsupported database type"}), 400





@dbRoute.route('/get-db-list',methods=['GET'])
@jwt_required()
def get_user_dbs():
    try:
        user = get_current_user()
        db_creds = DBCredentials.query.filter_by(user_id=user.id).all()
        db_creds_schema = BaseDBCredsSchema(many=True)
        return jsonify(db_creds_schema.dump(db_creds)), 200
    except SQLAlchemyError as err:
        return jsonify({"errors": err}), 400
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400


@dbRoute.route('/find-table-from-db',methods=['GET'])
@jwt_required()
def find_table_from_db():
    db_creds_id = request.args.get('db_creds_id', None, type=int)
    table_name = request.args.get('table_name', None, type=str)
    if not db_creds_id or table_name:
        return jsonify({"errors": "db_creds_id and table_name are required"}), 400
    user = get_current_user()
    db_creds = DBCredentials.query.filter_by(id=db_creds_id, user_id=user.id).first()
    if not db_creds:
        return jsonify({"errors": "db_creds_id is invalid or user not allowed to access DB"}), 400
    db_creds_schema = BaseDBCredsSchema(many=False)
    validated_data = db_creds_schema.dump(db_creds)
    validated_creds = prepare_creds(validated_data)
    db_type = validated_creds.pop('db_type', None)
    fetch_function = None
    if db_type == 'postgresql':
        fetch_function = fetch_table_exists_postgres
    elif db_type == 'mysql':
        fetch_function = fetch_table_exists_mysql
    if fetch_function:
        table_exists = asyncio.run(fetch_function(validated_creds, table_name))
        return jsonify(table_exists), 200
    else:
        return jsonify({"errors": "Unsupported database type"}), 400
    


    





