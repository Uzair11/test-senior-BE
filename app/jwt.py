from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
from app.models.user_model import User 
from . import jwt 

def set_jwt_callbacks():
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()