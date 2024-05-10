from flask import request, jsonify
from models.database import db
from models.course import Course
from __main__ import app

API_VERSION = 1

@app.route(f'/api/v{API_VERSION}/courses', methods=['GET'])
def get_courses():
    all_courses = Course.query.all()
    return jsonify([course.as_dict() for course in all_courses]), 200

@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = Course.query.get(course_id)
    
    if course is not None:
        return course.as_dict(), 200 
    else:
        return jsonify({"error": "Course not found"}), 404

@app.route(f'/api/v{API_VERSION}/courses', methods=['POST'])
def create_course():
    try:
        data = request.get_json()

        name=data.get('name')
        nr_videos=data.get('nr_videos')
        nr_teachers=data.get('nr_teachers')
        views=data.get('views')
        price=data.get('price')
        img_id=data.get('img_id')
        
        new_course = Course(
            name=name,
            nr_videos=nr_videos,
            nr_teachers=nr_teachers,
            views=views,
            price=price,
            img_id=img_id
        )
        
        db.session.add(new_course)
        db.session.commit()
        
        return jsonify({"message": "Course created successfully"}), 201
    
    except KeyError:
        return jsonify({"error": "Invalid request data"}), 400

@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    try:
        course = Course.query.get(course_id)
        
        if course is not None:
            data = request.get_json()
            
            course.name = data.get('name', course.name)
            course.nr_videos = data.get('nr_videos', course.nr_videos)
            course.nr_teachers = data.get('nr_teachers', course.nr_teachers)
            course.views = data.get('views', course.views)
            course.price = data.get('price', course.price)
            course.img_id = data.get('img_id', course.img_id)
 
            db.session.commit()
            return jsonify({"message": "Course updated successfully"}), 200
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        course = Course.query.get(course_id)
        
        if course is not None:
            password = request.headers.get('X-Delete-Password')
            
            if password == '12345678':
                db.session.delete(course)
                db.session.commit()
                return jsonify({"message": "Course deleted successfully"}), 200
            else:
                return jsonify({"error": "Incorrect password"}), 401
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500