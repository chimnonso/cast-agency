import os
import re
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db_name = "casting"
db_path = f"postgresql://postgres:foobar@localhost:5432/{db_name}"
db = SQLAlchemy()


def setup_db(app, db_path=db_path):

    uri = os.getenv('DATABASE_URL', db_path)
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)



class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(126), nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)
    actors = db.relationship('Actor', backref='actor', lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    # Insert into DB
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update a given record
    def update(self):
        db.session.commit()

    # Delete a record from DB
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }




class Actor(db.Model):
    __tablename__ = "actors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(126))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(126))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))


    def __init__(self, name, age, gender, movie_id):
        self.name = name 
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    # Insert into DB
    def insert(self):
        db.session.add(self)
        db.session.commit()

    # Update a given record
    def update(self):
        db.session.commit()

    # Delete a record from DB
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id,
        }

