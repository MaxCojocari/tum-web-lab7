from flask import request, jsonify
from models.database import db
from __main__ import app

API_VERSION = 1

@app.route(f'/v{API_VERSION}/api/courses', methods=['GET'])
def get_courses():
    return jsonify({"message": "List of courses"})
