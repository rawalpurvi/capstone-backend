import os
import json
import babel
from babel.dates import format_date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import (
    Column,
    String,
    Integer,
    Date,
    LargeBinary,
    create_engine
)

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
Actor_Movie

'''
# Implement many-to-many relationship using actor_movie with Actor and
# Movie tables


class Movie_Actor(db.Model):
    __tablename__ = 'movie_actor'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'actors.id',
            ondelete="CASCADE"),
        nullable=False)
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'movies.id',
            ondelete="CASCADE"),
        nullable=False)

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    movie_actors = db.relationship(
        'Movie_Actor',
        cascade="all, delete",
        backref='movies',
        lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        # Get actor detais for the movie
        selected_actors = []
        actors_info = db.session.query(
            Actor.id, Actor.name).filter(
            Movie_Actor.movie_id == self.id,
            Movie_Actor.actor_id == Actor.id).order_by(
            Actor.id).all()
        for actor in actors_info:
            selected_actors.append({
                "id": actor.id,
                "name": actor.name
            })

        # set release date in format
        formatDate = "EEEE, dd MMMM YYYY"
        format_release_date = babel.dates.format_date(
            self.release_date, formatDate)

        return {
            'id': self.id,
            'title': self.title,
            'release_date': format_release_date,
            'selected_actors': selected_actors
        }


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    movie_actors = db.relationship(
        'Movie_Actor',
        cascade="all, delete",
        backref='actors',
        lazy=True)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age
        }
