from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from auth.auth import AuthError, requires_auth
from database.models import Actor, Movie, setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)


# ROUTES
# --------------------Movies----------------

# Get all the movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def getAllMovies(payload):
        movies = Movie.query.all()

        serialized_movies = []
        for movie in movies:
            serialized_movie = {
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None
            }
            serialized_movies.append(serialized_movie)

        return jsonify({
            'success': True,
            'movies': serialized_movies
        }), 200

    # Get movie by ID

    @app.route('/movies/<int:id>')
    @requires_auth('get:movies')
    def getByMovieId(payload, id):
        movie = Movie.query.get(id)

        if not movie:
            return jsonify(
                {'success': False, 'error': 'Movie Not Found'}), 404

        serialized_movie = {
            'id': movie.id,
            'title': movie.title,
            'release_date': movie.release_date.strftime('%Y-%m-%d') if movie.release_date else None
        }

        return jsonify({
            'success': True,
            'movies': serialized_movie
        }), 200

    # Create new Movie

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def createMovie(payload):
        try:
            body = request.json
            new_movie = Movie(title=body['title'],
                              release_date=body['release_date'])
            Movie.insert(new_movie)

            return jsonify({
                'success': True,
                'movies': new_movie.title
            }), 200

        except:
            abort(400)

    # Update the existing movie detail

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def updateMovie(payload, id):
        try:
            body = request.json
            movie = Movie.query.get(id)

            if not movie:
                abort(404)

            title = body['title']
            release_date = body['release_date']
            Movie.update(movie, title, release_date)

            return jsonify({
                'success': True,
                'movie': movie.title
            }), 200

        except Exception as e:
            print(e)
            return jsonify(
                {'success': False, 'error': 'Failed to update movie'}), 500

    # Delete the created movie

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def deleteMovie(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if not movie:
            abort(404)

        try:
            Movie.delete(movie)
            return jsonify({
                'success': True,
                'deleted_movie': id
            }), 200

        except:
            abort(422)

    # --------------------------ACTOR--------------------------

    # Get all Actors details

    @app.route('/actors')
    @requires_auth('get:actors')
    def getAllActors(payload):
        actors = Actor.query.all()

        serialized_actors = []
        for actor in actors:
            serialized_actor = {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            }
            serialized_actors.append(serialized_actor)

        return jsonify({
            'success': True,
            'actors': serialized_actors
        }), 200

    # Get Actor By ID

    @app.route('/actors/<int:id>')
    @requires_auth('get:actors')
    def getByActorId(payload, id):
        actor = Actor.query.get(id)

        if not actor:
            return jsonify(
                {'success': False, 'error': 'Actor Not Found'}), 404

        serialized_actor = {
            'id': actor.id,
            'name': actor.name,
            'age': actor.age,
            'gender': actor.gender
        }

        return jsonify({
            'success': True,
            'movies': serialized_actor
        }), 200

    # Create new Actor details

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def createActor(payload):
        try:
            body = request.json
            new_actor = Actor(name=body['name'],
                              age=body['age'],
                              gender=body['gender'])
            Actor.insert(new_actor)

            return jsonify({
                'success': True,
                'name': new_actor.name,
                'age': new_actor.age,
                'gender': new_actor.gender
            }), 200

        except:
            abort(400)

    # Update the existing Actor details

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def updateActor(payload, id):
        try:
            body = request.json
            actor = Actor.query.get(id)

            if not actor:
                abort(404)

            name = body['name']
            age = body['age']
            gender = body['gender']
            Actor.update(actor, name, age, gender)

            serialized_actor = {
                'id': actor.id,
                'name': actor.name,
                'age': actor.age,
                'gender': actor.gender
            }

            return jsonify({
                'success': True,
                'actor': serialized_actor
            }), 200

        except:
            abort(500)

    # Delete the created Actor details

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def deleteActor(payload, id):

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if not actor:
            abort(404)

        try:
            Actor.delete(actor)
            return jsonify({
                'success': True,
                'deleted_actor': id
            }), 200

        except:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        return jsonify({
            "success": False,
            "error": auth_error.status_code,
            "message": auth_error.error
        }), auth_error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    @app.errorhandler(500)
    def serverError(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500


app = create_app()
if __name__ == "__main__":
    app.run()
