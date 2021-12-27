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
			'Content-Type, Authorization,true'
		)
		response.headers.add(
			'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS'
		)

		return response

	@app.route('/test')
	def testing():
		return jsonify({
            "success": True,
            "message": "welcome"
        })

	return app

app = create_app()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80, debug=True)