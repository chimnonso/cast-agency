import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class CastingAgencyTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app()
		self.excutive_producer_token = os.environ['executive_producer_token']
		self.casting_director_token = os.environ['casting_director_token']
		self.casting_assistant_token = os.environ['casting_assistant_token']
		self.client = self.app.test_client
		self.dbase_name = "casting_agency_test"
		self.dbase_path = f"postgresql://postgres:foobar@localhost:5432/{self.dbase_name}"
		
		setup_db(self.app, self.dbase_path)
		
		with self.app.app_context():
			self.db = SQLAlchemy()
			self.db.init_app(self.app)
			self.db.create_all()
			
			
		self.movie = {
            "title": "My movie",
            "release_date": "3030-12-30"
        }
		
		
		self.actor = {
            "name": "John smith",
            "age": 30,
            "gender": "M",
            "movie_id": 5,
        }
		
		
		def tearDown(self):
			pass
			
	def test_get_movies(self):

		header_obj = {
			"Authorization": f"Bearer {self.casting_assistant_token}"
		}

		res = self.client().get('/movies', headers=header_obj)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data['success'])

	def test_get_movies_404(self):
		header_obj = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }
		res = self.client().get('/moviessss', headers=header_obj)
		data = json.loads(res.data)
		
		self.assertEqual(res.status_code, 404)
		self.assertEqual(data["success"], False)
		self.assertEqual(data["message"], "not found")

	def test_create_movie(self):
		header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }

		res = self.client().post('/movies',
								json=self.movie, headers=header_obj)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertTrue(data["success"])









	def test_get_actors(self):
		header_obj = {
            "Authorization": f"Bearer {self.casting_director_token}"
        }

		res = self.client().get('/actors', headers=header_obj)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data["success"], True)
		self.assertIn('actors', data)
	
	
	def test_get_actors_404(self):
		header_obj = {
            "Authorization": f"Bearer {self.casting_director_token}"
        }

		res = self.client().get('/actorssssssss', headers=header_obj)
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 404)
		self.assertEqual(data["success"], False)
		self.assertEqual(data["message"], "not found")





if __name__ == "__main__":
    unittest.main()