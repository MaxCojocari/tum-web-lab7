from flask import request, jsonify
from models.database import db
from models.course import Course
from __main__ import app

API_VERSION = 1

@app.route(f'/api/v{API_VERSION}/courses', methods=['GET'])
def get_courses():
    try:
        all_courses = Course.query.all()
        return jsonify([course.as_dict() for course in all_courses]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    try:
        course = Course.query.get(course_id)
        
        if course is not None:
            return course.as_dict(), 200 
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/courses', methods=['POST'])
def create_course():
    try:
        data = request.get_json(silent=True) or {}

        required_fields = ['name', 'nr_videos', 'nr_teachers', 'views', 'price', 'img_id']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required data fields"}), 400

        new_course = Course(**data)
        db.session.add(new_course)
        db.session.commit()
        
        return jsonify({"message": "Course created successfully"}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    
    data = request.get_json()
    try:      
        course.name = data.get('name', course.name)
        course.nr_videos = data.get('nr_videos', course.nr_videos)
        course.nr_teachers = data.get('nr_teachers', course.nr_teachers)
        course.views = data.get('views', course.views)
        course.price = data.get('price', course.price)
        course.img_id = data.get('img_id', course.img_id)

        db.session.commit()
        return jsonify({"message": "Course updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    
    password = request.headers.get('X-Delete-Password')
    if not password or password != '12345678':
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500