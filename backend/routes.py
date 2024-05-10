from flask import request, jsonify
from models.database import db
from models.course import Course
from __main__ import app

API_VERSION = 1

@app.route(f'/api/v{API_VERSION}/courses', methods=['GET'])
def get_courses():
    all_courses = Course.query.all()
    return jsonify([course.as_dict() for course in all_courses]), 200
