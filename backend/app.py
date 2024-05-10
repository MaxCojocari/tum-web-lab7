from flask import Flask
from models.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['JWT_SECRET_KEY'] = 'ww%JlM}wa&"q10' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    app.config['SWAGGER'] = {
        "title": "CourseMe API",
        "version": '0.1',
        "description": "This is API description for CourseMe app.",
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
    Swagger(app) 
    JWTManager(app)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()