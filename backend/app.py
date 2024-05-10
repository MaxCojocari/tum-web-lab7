from flask import Flask
from models.database import db
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['JWT_SECRET_KEY'] = 'ww%JlM}wa&"q10' 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60
    
    JWTManager(app)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()