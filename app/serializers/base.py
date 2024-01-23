from marshmallow_sqlalchemy import SQLAlchemyAutoSchema as ModelSchema
from marshmallow import fields, validates_schema, ValidationError
from app.models.db_creds import DBCredentials
from app.models.user_model import User


class BaseDBCredsSchema(ModelSchema):
    class Meta:
        model = DBCredentials
        load_instance = True
        include_fk = True

    host = fields.Str(required=True)

    @validates_schema
    def validate_host(self, data, **kwargs):
        host = data.get('host')
        if host:
            if host == 'localhost':
                raise ValidationError("Cannot establish connection with localhost")
            return True
        raise ValidationError("Host not specified")

    @validates_schema()
    def validate_db_type(self, data, **kwargs):
        db_type = data.get('db_type')
        if db_type:
            if db_type not in ['postgresql', 'mysql']:
                raise ValidationError("Database type must be postgresql or mysql")
            return True
        raise ValidationError("Database type must be postgresql or mysql")


class BaseUserSerializer(ModelSchema):
    class Meta:
        model = User
        load_instance = True
        