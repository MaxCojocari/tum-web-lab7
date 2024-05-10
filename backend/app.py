from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.course import Course

def create_app():
    app = Flask(__name__)
    
    # Configure SQLAlchemy to use SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    db.init_app(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run()