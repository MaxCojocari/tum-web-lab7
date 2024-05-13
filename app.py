from flask import Flask
from models.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['JWT_SECRET_KEY'] = 'ww%JlM}wa&"q10' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False # for https should be set to True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False # True, for production use
    app.config['SWAGGER'] = {
        "title": "CourseMe API",
        "version": '0.1',
        "description": "This is description for CourseMe API.",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
    Swagger(app) 
    JWTManager(app)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()