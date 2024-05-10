from app import create_app, db, Course
from init_courses import COURSES

def init_database():
    app = create_app()
    
    with app.app_context():
        db.create_all()
        
        for course in COURSES:
            sample_course = Course(
                name=course["name"],
                nr_videos=course["nr_videos"],
                nr_teachers=course["nr_teachers"],
                views=course["views"],
                price=course["price"],
                img_id=course["img_id"]
            )
            db.session.add(sample_course)
        
        db.session.commit()

if __name__ == "__main__":
    init_database()