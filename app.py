import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Actor, Movie, Movie_Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    @ADD:
    Create an endpoint to handle GET requests
    for actors.
    '''
    # get actors
    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors_info = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actors_info]

        # if there is no actor added
        if len(actors_info) == 0:
            abort(404)

        # retrun array of actors details
        return jsonify({
            'success': True,
            'actors': actors
        })

    '''
    @ADD:
    Create an endpoint to handle GET requests
    for movies.
    '''
    # get movies
    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies_info = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in movies_info]

        # if there is no movie added
        if len(movies_info) == 0:
            abort(404)

        # retrun array of movies details
        return jsonify({
            'success': True,
            'movies': movies
        })

    '''
    @ADD:
    Create an endpoint to handle POST requests
    for actors.
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(actor):
        body = request.get_json()
        try:
            # Add new actor
            new_name = body.get("name", None)
            new_age = body.get("age", None)
            new_gender = body.get("gender", None)
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            # Get inserted new actor details
            new_actor = Actor.query.order_by(Actor.id.desc()).limit(1).first()
            new_actor = new_actor.format()

            return jsonify({
                'success': True,
                'actors': new_actor
            })
        except BaseException:
            abort(422)

    '''
    @ADD:
    Create an endpoint to handle POST requests
    for movies.
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(movie):
        body = request.get_json()
        try:
            # Add new movie
            new_title = body.get("title", None)
            new_release_date = body.get("release_date", None)
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            # Get inserted new movie details
            new_movie = Movie.query.order_by(Movie.id.desc()).limit(1).first()
            new_movie = new_movie.format()

            return jsonify({
                'success': True,
                'movies': new_movie
            })
        except BaseException:
            abort(422)

    '''
    @ADD:
    Create an endpoint to handle PATCH requests
    for actors.
    '''
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(actor, actor_id):
        body = request.get_json()
        try:
            name = body.get("name", None)
            gender = body.get("gender", None)
            age = body.get("age", None)

            # Update Actor
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

            if actor is None:
                abort(404)

            if name:
                actor.name = name
            if gender:
                actor.gender = gender
            if age:
                actor.age = age

            actor.update()
            updated_actor = actor.format()

            return jsonify({
                'success': True,
                'actors': [updated_actor]
            })

        except BaseException:
            abort(400)

    '''
    @ADD:
    Create an endpoint to handle PATCH requests
    for movies.
    '''
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(movie, movie_id):
        body = request.get_json()
        try:
            title = body.get("title", None)
            release_date = body.get("release_date", None)
            actor_ids = body.get("selected_actors", None)

            # Update Movie
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date

            movie.update()
            updated_movie = movie.format()

            # Check actors are already assigned
            movie_actors = Movie_Actor.query.filter(
                Movie_Actor.movie_id == movie_id).all()
            if movie_actors:
                for movie_actor in movie_actors:
                    movie_actor.delete()

            # Set updated movie id and actor id in movie_actor table
            if actor_ids:
                for actor_id in actor_ids:
                    movie_actor = Movie_Actor(
                        movie_id=movie_id, actor_id=actor_id)
                    movie_actor.insert()

            return jsonify({
                'success': True,
                'drinks': [updated_movie]
            })

        except BaseException:
            abort(400)

    '''
    @ADD:
    Create an endpoint to handle DELETE requests
    for actors.
    '''
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor, actor_id):

        try:
            # Delete Actor
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)

            actor.delete()

            return jsonify({
                'success': True,
                'delete': actor_id
            })

        except BaseException:
            abort(400)

    '''
    @ADD:
    Create an endpoint to handle DELETE requests
    for movies.
    '''
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie, movie_id):

        try:
            # Delete Movie
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'delete': movie_id
            })

        except BaseException:
            abort(400)

    '''
    @ADD:
    Error Handling
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": " A generic error occurred on the server"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    '''
    @ADD: implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error
        }), ex.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
