import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)