import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


from models import Movie, Actor, setup_db
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
	
	app = Flask(__name__)
	setup_db(app)
	CORS(app)

	@app.after_request
	def after_request(response):
		response.headers.add(
			'Access-Control-Allow-Headers',
			'Content-Type,Authorization'
		)
		response.headers.add(
			'Access-Control-Allow-Methods',
            'GET,POST,PATCH,DELETE,OPTIONS'
		)

		return response

	@app.route('/test')
	def testing():
		return jsonify({
            "success": True,
            "message": "welcome"
        })

	@app.route('/movies')
	@requires_auth('get:movies')
	def get_movies(payload):
		movies_query = Movie.query.all()

		movies = [movie.format() for movie in movies_query]

		return jsonify({
			"success": True,
			"movies": movies
		})

	@app.route('/movies', methods=["POST"])
	@requires_auth('post:movie')
	def create_movie(payload):
		
		body = request.get_json()
			
		if body is None:
			abort(400)
			
		title = body.get('title', None)
		release_date = body.get('release_date', None)

		if title is None or release_date is None:
			abort(400)

		movie = Movie(
			title= title,
			release_date=release_date
		)
		movie.insert()

		return jsonify({
			"success": True,
		})

	@app.route('/movies/<int:movie_id>', methods=['PATCH'])
	@requires_auth('patch:movie')
	def update_movie(payload, movie_id):

		updated_movie = Movie.query.get(movie_id)
		if updated_movie is None:
			abort(404)

		body = request.get_json()
		title = body.get('title', None)
		release_date = body.get('release_date', None)

		if title:
			updated_movie.title = title
		
		if release_date:
			updated_movie.release_date = release_date

		updated_movie.update()

		return jsonify({
			"success": True,
			"updated_movie_id": updated_movie.id,
			"updated_movie_title": updated_movie.title
		})
	
	@app.route('/movies/<int:movie_id>', methods=["DELETE"])
	@requires_auth('delete:movie')
	def delete_movie(payload, movie_id):
		movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

		if movie is None:
			abort(404)

		movie.delete()

		return jsonify({
			"success": True,
			"deleted_movie_id": movie.id
		})



	'''
	All Actors endpoints

	'''


	@app.route('/actors', methods=['GET'])
	@requires_auth('get:actors')
	def get_actors(payload):

		actors_query = Actor.query.order_by(Actor.id).all()

		actors = [actor.format() for actor in actors_query]

		return jsonify({
			"success": True,
			"actors": actors
		})
	
	@app.route('/actors', methods=["POST"])
	@requires_auth('post:actor')
	def create_actor(payload):
		body = request.get_json()

		if body is None:
			abort(400)

		name = body.get('name', None)
		age = body.get('age', None)
		gender = body.get('gender', None)
		movie_id = body.get('movie_id', None)

		if name is None or age is None or gender is None or movie_id is None:
			abort(400)

		actor = Actor(
			name=name,
			age=age,
			gender=gender,
			movie_id=movie_id,
		)

		actor.insert()

		return jsonify({
			"success": True,
		})


	@app.route('/actors/<int:actor_id>', methods=["PATCH"])
	@requires_auth('patch:actor')
	def update_actor(payload, actor_id):
		actor = Actor.query.get(actor_id)

		if not actor:
			abort(404)

		body = request.get_json()


		name = body.get('name', None)
		age = body.get('age', None)
		gender = body.get('gender', None)
		movie_id = body.get('movie_id', None)

		if name is None and age is None and gender is None and movie_id is None:
			abort(422)

		if name:
			actor.name = name
		if age:
			actor.age = age
		if gender:
			actor.gender = gender
		if movie_id:
			actor.movie_id = movie_id

		try:
			actor.update()
		except:
			abort(400)

		return jsonify({
			"success": True,
			"updated_actor_id": actor.id,
			"updated_actor_name": actor.name
		})


	@app.route('/actors/<int:actor_id>', methods=["DELETE"])
	@requires_auth('delete:actor')
	def delete_actor(payload, actor_id):
		actor = Actor.query.get(actor_id)

		if actor is None:
			abort(404)

		try:
			actor.delete()

			return jsonify({
				"success": True,
				"deleted_actor_id": actor.id
			})
		
		except Exception:
			abort(500)





	

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			"success": False,
			"message": "bad request",
			"error": 400,
		}), 400

	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			"success": False,
			"message": "not found",
			"error": 404,
		}), 404
		

	@app.errorhandler(422)
	def not_found(error):
		return jsonify({
			"success": False,
			"message": "unprocessable",
			"error": 422,
		}), 422

	@app.errorhandler(AuthError)
	def auth_error(auth_error):
		return jsonify({
			"success": False,
			"error": auth_error.status_code,
			"message": auth_error.error['description']
		})

	@app.errorhandler(500)
	def internal_error(error):
		return jsonify({
			"success": False,
			"message": "internal error",
			"error": 500,
		}), 500




	return app

app = create_app()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)