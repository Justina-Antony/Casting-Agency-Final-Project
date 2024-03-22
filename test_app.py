import os
import unittest
import json
from app import create_app
from database.models import setup_db
from constants import executive_producer, invalid_token
# from dotenv import load_dotenv

class CastingTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(active=False)
        self.app.app_context().push()
        self.client = self.app.test_client
        self.database_name = "postgres"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "postgres", "root", "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_movies_200(self):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_movies_with_invalid_token(self):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(invalid_token)
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_post_movies_200(self):

        new_movie = {
            'title': 'Hello World',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_post_movies_null(self):

        new_movie = {
            'title': '',
            'release_date': '2017-10-20'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().post('/movies', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


    def test_patch_movies_200(self):

        new_movie = {
            'title': 'Wonderful',
            'release_date': '2022-05-29'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().patch('/movies/2', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_not_found(self):

        new_movie = {
            'title': 'Wonderful',
            'release_date': '2022-05-29'
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().patch('/movies/100', json=new_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movies_200(self):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().delete('/movies/4', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_not_found(self):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer {}".format(executive_producer)
        }
        res = self.client().delete('/movies/4', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()