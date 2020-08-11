import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://postgres:postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Setup default categories
        self.categories = [
            {
                'id': 1,
                'type': 'Science'
            },
            {
                'id': 2,
                'type': 'Art'
            },
            {
                'id': 3,
                'type': 'Geography'
            },
            {
                'id': 4,
                'type': 'History'
            },
            {
                'id': 5,
                'type': 'Entertainment'
            },
            {
                'id': 6,
                'type': 'Sports'
            },
            {
                'id': 1,
                'type': 'Science'
            },
        ]

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        for index, category in enumerate(data['categories']):
            self.assertEqual(category['id'], self.categories[index]['id'])
            self.assertEqual(category['type'], self.categories[index]['type'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()