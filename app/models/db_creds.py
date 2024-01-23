from .user_model import User
from . import db


class DBCredentials(db.Model):
    __tablename__ = 'db_credentials'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    host = db.Column(db.String(55), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    db_name = db.Column(db.String(55), nullable=False)
    username = db.Column(db.String(55), nullable=False)
    password = db.Column(db.String(55), nullable=False)
    db_type = db.Column(db.String(55), nullable=False)
