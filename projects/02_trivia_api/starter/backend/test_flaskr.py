import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

def helper_valid_get_questions(self, res):
    data = json.loads(res.data)

    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['success'])
    self.assertEqual(data['total_questions'], Question.query.count())
    self.assertEqual(len(data['questions']), 10)
    self.assertIsNone(data['current_category'])

    categories = data['categories']
    for key in categories:
        self.assertEqual(categories[key], self.categories[key])


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
        self.categories = {
                '1': 'Science',
                '2': 'Art',
                '3': 'Geography',
                '4': 'History',
                '5': 'Entertainment',
                '6': 'Sports',
                '7': 'Science'
            }


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
        categories = data['categories']
        for key in categories:
            self.assertEqual(categories[key], self.categories[key])
    
    def test_get_questions_no_page(self):
        res = self.client().get('/questions')
        helper_valid_get_questions(self, res)
        

    def test_get_questions_valid_page(self):
        res = self.client().get('/questions?page=1')
        helper_valid_get_questions(self, res)

    def test_get_questions_invalid_page(self):
        res = self.client().get('questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "not found")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()