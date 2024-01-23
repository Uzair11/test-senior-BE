from . import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=20), nullable=False)
    password = db.Column(db.String(44), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    db_creds = db.relationship('DBCredentials', backref='User', lazy=True)
