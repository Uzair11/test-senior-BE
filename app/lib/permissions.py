from app.models.db_creds import DBCredentials
from app.models.user_model import User

def check_db_permission(user_id,db_cred_id) -> bool:
    # used to check if the user has permission to access the database credentials
    try:
        db_cred = DBCredentials.query.filter_by(id=db_cred_id,user_id=user_id).first()
        if db_cred:
            return True
        else:
            return False
    except:
        return False
