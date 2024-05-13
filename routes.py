from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.database import db
from models.course import Course
from __main__ import app
from flasgger import swag_from

API_VERSION = 1
DEFAULT_USER_ID = 1

@app.route(f'/api/v{API_VERSION}/courses', methods=['GET'])
@jwt_required()
@swag_from('swagger_yaml/get_all.yaml')
def get_courses():
    claims = get_jwt()
    
    if 'READ' not in claims.get('permissions', []):
        return jsonify({'message': 'Permission denied'}), 403
      
    try:
        ids = request.args.get('ids')
        limit = request.args.get('limit', default=None, type=int)
        offset = request.args.get('offset', default=None, type=int)

        if ids:
            ids = list(map(int, ids.split(',')))
            paginated_courses = Course.query.filter(Course.id.in_(ids)).offset(offset).limit(limit).all()
            if not paginated_courses:
                return jsonify({"error": "Courses not found"}), 404
        else:
            paginated_courses = Course.query.offset(offset).limit(limit).all()

        courses_data = [course.as_dict() for course in paginated_courses]
        
        return jsonify(courses_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/courses/<int:course_id>', methods=['GET'])
@jwt_required()
@swag_from('swagger_yaml/get.yaml')
def get_course_by_id(course_id):
    claims = get_jwt()
    
    if 'READ' not in claims.get('permissions', []):
        return jsonify({'message': 'Permission denied'}), 403

    try:
        course = Course.query.get(course_id)
        
        if course is not None:
            return course.as_dict(), 200 
        else:
            return jsonify({"error": "Course not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/courses', methods=['POST'])
@jwt_required()
@swag_from('swagger_yaml/post.yaml')
def create_course():
    claims = get_jwt()
    
    if 'WRITE' not in claims.get('permissions', []):
        return jsonify({'message': 'Permission denied'}), 403
    
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
@jwt_required()
@swag_from('swagger_yaml/put.yaml')
def update_course(course_id):
    claims = get_jwt()
    
    if 'UPDATE' not in claims.get('permissions', []):
        return jsonify({'message': 'Permission denied'}), 403
    
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
@jwt_required()
@swag_from('swagger_yaml/delete.yaml')
def delete_course(course_id):
    claims = get_jwt()
    
    if 'DELETE' not in claims.get('permissions', []):
        return jsonify({'message': 'Permission denied'}), 403
    
    course = Course.query.get(course_id)
    if course is None:
        return jsonify({"error": "Course not found"}), 404
    
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route(f'/api/v{API_VERSION}/token', methods=['POST'])
@swag_from('swagger_yaml/create_token.yaml')
def create_token():
    try:
        data = request.get_json(silent=True) or {}

        required_fields = ['permissions']
        
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required data fields"}), 400
        
        user_id = data.get('user_id', DEFAULT_USER_ID)
        additional_claims = {
            'permissions': data.get('permissions')
        }
        
        access_token = create_access_token(identity=user_id, additional_claims=additional_claims)
        response = jsonify({"jwt": access_token})
        response.set_cookie('access_token_cookie', access_token, httponly=True, secure=False, samesite='Lax', max_age=3600)  # for production, set secure=True
        return response, 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500