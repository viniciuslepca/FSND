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

def helper_error(self, res, data, error, message):
    self.assertEqual(res.status_code, error)
    self.assertFalse(data['success'])
    self.assertEqual(data['error'], error)
    self.assertEqual(data['message'], message)

def helper_error_400(self, res, data):
    helper_error(self, res, data, 400, 'bad request')

def helper_error_404(self, res, data):
    helper_error(self, res, data, 404, 'not found')

def helper_error_405(self, res, data):
    helper_error(self, res, data, 405, 'method not allowed')


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

        self.question = {
            'question': "Which Jamaican runner is an 11-time world champion and holds the record in the 100 and 200-meter race?",
            'answer': "Usain Bolt",
            'difficulty': 1,
            'category': 6
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
        res = self.client().get('/questions?page={}'.format(10000))
        data = json.loads(res.data)

        helper_error_404(self, res, data)

    def test_delete_valid_question(self):
        question = Question(**self.question)
        question.insert()
        id = question.id
        original_count = Question.query.count()

        res = self.client().delete('/questions/{}'.format(id))
        data = json.loads(res.data)
        deleted_question = Question.query.filter(Question.id == id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertIsNone(deleted_question)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], original_count - 1)
        self.assertEqual(data['deleted'], id)

    def test_delete_invalid_question(self):
        original_count = Question.query.count()
        res = self.client().delete('/questions/{}'.format(10000))
        data = json.loads(res.data)
        new_count = Question.query.count()
        self.assertEqual(new_count, original_count)

        helper_error_404(self, res, data)

    def test_create_new_question(self):
        original_count = Question.query.count()
        res = self.client().post('/questions', json=self.question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], original_count + 1)
        added_question = Question.query.filter(Question.id == data['created']).one_or_none()
        self.assertIsNotNone(added_question)

    def test_create_new_question_invalid_route(self):
        original_count = Question.query.count()
        res = self.client().post('/questions/1', json=self.question)
        data = json.loads(res.data)

        helper_error_405(self, res, data)

    def test_create_new_question_no_body(self):
        original_count = Question.query.count()
        res = self.client().post('/questions')
        data = json.loads(res.data)

        helper_error_400(self, res, data)







# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()