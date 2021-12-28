import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class AgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.dbase_name = "casting_agency_test"
        self.dbase_path = f"postgresql://postgres:foobar@localhost:5432/{self.dbase_name}"

        setup_db(self.app, self.dbase_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.excutive_producer_token = os.environ['executive_producer_token']
        self.casting_director_token = os.environ['casting_director_token']
        self.casting_assistant_token = os.environ['casting_assistant_token']

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
        # print(res)
        data = json.loads(res.data)
        # print(data)

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

    def test_create_movie_fail_400(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }

        invalid_movie = {"title": None, "release_date": None}
        res = self.client().post('/movies',
                                    json=invalid_movie, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    # def test_delete_movie(self):
    #     header_obj = {
    # 		"Authorization": f"Bearer {self.excutive_producer_token}"
    # 	}
    # 	movie_id = 11
    # 	res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
    # 	data = json.loads(res.data)
    # 	self.assertEqual(res.status_code, 200)
    # 	self.assertEqual(data["success"], True)
    # 	self.assertEqual(data['deleted_movie_id'], movie_id)

    def test_delete_movie_404(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        movie_id = -100
        res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')

    def test_update_movie(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        movie_id = 1
        new_title = "Updated Title"
        res = self.client().patch(f'/movies/{movie_id}',
                            json={'title': new_title}, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated_movie_id"], movie_id)
        self.assertEqual(data["updated_movie_title"], new_title)

    def test_update_movie_404(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        movie_id = -1
        new_title = "Updated Title"
        res = self.client().patch(f'/movies/{movie_id}', json={'title': new_title}, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not found")

    # def test_delete_movie_403(self):
    # 	header_obj = {
    # 		"Authorization": f"Bearer {self.casting_assistant_token}"
    # 	}

    # 	movie_id = 1
    # 	res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
    # 	data = json.loads(res.data)
    # 	print(data)

    # 	self.assertEqual(res.status_code, 403)
    # 	self.assertEqual(data["success"], False)
    # 	self.assertEqual(data['message'], 'Permission not found')

    def test_get_actors(self):
        header_obj = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }

        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIn('actors', data)

    def test_get_actors_404(self):
        header_obj = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }

        res = self.client().get('/actorssssssss', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not found")

    def test_create_actor(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }

        res = self.client().post('/actors',
                                    json=self.actor, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_actor_fail_400(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        invalid_actor = {"name": None, "gender": None}

        res = self.client().post('/actors',
                                    json=invalid_actor, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "bad request")

    # def test_delete_actor(self):
    # 	header_obj = {
    # 		"Authorization": f"Bearer {self.excutive_producer_token}"
    # 	}
    # 	actor_id = 8
    # 	res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
    # 	data = json.loads(res.data)

    # 	self.assertEqual(res.status_code, 200)
    # 	self.assertEqual(data["success"], True)
    # 	self.assertEqual(data['deleted_actor_id'], actor_id)

    def test_delete_actor_404(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        actor_id = 100000000000000000000
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "not found")

    def test_delete_actor_403(self):
        header_obj = {
            "Authorization": f"Bearer {self.casting_assistant_token}"
        }
        actor_id = 2
        # print(header_obj)
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Permission not found')

    def test_update_actor(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        actor_id = 1
        new_name = "New Name"
        res = self.client().patch(f'/actors/{actor_id}',
                                    json={'name': new_name}, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["updated_actor_id"], actor_id)
        self.assertEqual(data["updated_actor_name"], new_name)

    def test_update_actor_422(self):
        header_obj = {
            "Authorization": f"Bearer {self.excutive_producer_token}"
        }
        actor_id = 1
        invalid_actor = {}
        res = self.client().patch(f'/actors/{actor_id}',
                                json=invalid_actor, headers=header_obj)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

if __name__ == "__main__":
    unittest.main()
