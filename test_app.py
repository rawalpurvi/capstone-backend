import os
import unittest
import json
import urllib.request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt

from app import create_app
from models import setup_db, Actor, Movie, Movie_Actor
from auth import AuthError, requires_auth


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_TEST_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Create New Movie
        self.new_movie = {
            'title': 'Air Force One',
            'release_date': '1997-07-25'
        }

        # Create New Actor
        self.new_actor = {
            'name': 'Leonardo DiCaprio',
            'age': 46,
            'gender': 'Male'
        }

        self.executive_producer_jwt = {
                    'Authorization': "Bearer $Token"
                    }
        self.casting_director_jwt = {
                    'Authorization': "Bearer $Token"
                    }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    @ADD
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    # Run test to get Actors and Error occures

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_405_if_actor_not_found(self):
        res = self.client().get('/actors/35')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to get Movies and Error occures

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_405_if_movie_not_found(self):
        res = self.client().get('/movies/35')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to add Actor and Error occures

    def test_add_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.executive_producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    def test_405_if_actor_addition_not_allowed(self):
        res = self.client().post('/actors/45', json=self.new_actor,
                                 headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to update Actor and Error occures

    def test_update_actor_age(self):
        res = self.client().patch(
            'actors/8', json={'age': 46}, headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 8).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor.format()['age'], 46)

    def test_400_for_failed_actor_update(self):
        res = self.client().patch(
            '/actors/101', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test to delete Actor and Error occures

    def test_delete_actor(self):
        res = self.client().delete(
            'actors/5', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        actor = Actor.query.filter(Actor.id == 5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 5)
        self.assertEqual(actor, None)

    def test_400_if_actor_does_not_exit(self):
        res = self.client().delete(
            '/actors/1000', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test for Role base casting director doesn't have permission to add
    # movie

    def test_unauthorize_for_add_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.casting_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    # Run test to add Movie and Error occures

    def test_add_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.executive_producer_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

    def test_405_if_movie_addition_not_allowed(self):
        res = self.client().post('/movies/45', json=self.new_movie,
                                 headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to update Movie and Error occures

    def test_update_movie_title(self):
        res = self.client().patch('movies/6',
                                  json={'title': 'Lord OF The Rings'},
                                  headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie.format()['title'], 'Lord OF The Rings')

    def test_400_for_failed_movie_update(self):
        res = self.client().patch(
            '/movies/101', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test to assign Actors to the Movie

    def test_assign_actors_to_movie(self):
        res = self.client().patch(
            'movies/6',
            json={
                'selected_actors': [
                    '10',
                    '11']},
            headers=self.casting_director_jwt)
        data = json.loads(res.data)
        movie_actors = Movie_Actor.query.filter(
            Movie_Actor.movie_id == 6).all()
        selected_actors = []
        if movie_actors:
            selected_actors = [str(movie_actor.actor_id)
                               for movie_actor in movie_actors]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(selected_actors, ['10', '11'])

    # Run test for Role base casting director doesn't have permission to
    # delete movie

    def test_unauthorize_for_delete_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.casting_director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    # Run test to delete Movie and Error occures

    def test_delete_movie(self):
        res = self.client().delete(
            'movies/5', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        movie = Movie.query.filter(Movie.id == 5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 5)
        self.assertEqual(movie, None)

    def test_400_if_movie_does_not_exit(self):
        res = self.client().delete(
            '/movies/1000', headers=self.executive_producer_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
