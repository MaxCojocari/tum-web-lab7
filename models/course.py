from models.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nr_videos = db.Column(db.Integer, nullable=False)
    nr_teachers = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img_id = db.Column(db.String(100), nullable=False)

    def __init__(self, name, nr_videos, nr_teachers, views, price, img_id):
        self.name = name
        self.nr_videos = nr_videos
        self.nr_teachers = nr_teachers
        self.views = views
        self.price = price
        self.img_id = img_id

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'nr_videos': self.nr_videos,
            'nr_teachers': self.nr_teachers,
            'views': self.views,
            'price': self.price,
            'img_id': self.img_id
        }