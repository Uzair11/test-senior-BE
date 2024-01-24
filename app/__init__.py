import logging
from flask import Flask
from flask_migrate import Migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from app.models import db
from app.routes import auth_routes, db_routes

logging.basicConfig(filename='record.log', level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

jwt = JWTManager()
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.DevelopmentConfig')
    app.logger.setLevel(logging.ERROR)  
    handler = logging.StreamHandler() 
    app.logger.addHandler(handler)
    jwt.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.reflect()
        db.create_all()
    migrate = Migrate()
    migrate.init_app(app, db)
    from app.jwt import set_jwt_callbacks
    set_jwt_callbacks()
    Swagger(app)
    app.register_blueprint(auth_routes.authRoute, url_prefix='/auth')
    app.register_blueprint(db_routes.dbRoute, url_prefix='/db')
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')



