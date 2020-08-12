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
    self.assertTrue(len(data['questions']) <= 10)
    self.assertIsNone(data['current_category'])

    categories = data['categories']
    for key in categories:
        self.assertEqual(categories[key], self.categories[key])

def helper_error(self, res, data, error):
    self.assertEqual(res.status_code, error)
    self.assertFalse(data['success'])
    self.assertEqual(data['error'], error)
    error_to_message = {
        400: 'bad request',
        404: 'not found',
        405: 'method not allowed',
        422: 'unprocessable entity'
    }
    self.assertEqual(data['message'], error_to_message[error])

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
    DONE
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

        helper_error(self, res, data, 404)

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

        helper_error(self, res, data, 404)

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

        helper_error(self, res, data, 405)

    def test_create_new_question_no_body(self):
        original_count = Question.query.count()
        res = self.client().post('/questions')
        data = json.loads(res.data)

        helper_error(self, res, data, 400)

    def test_search_question_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'what'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], Question.query.filter(Question.question.ilike('%what%')).count())
        self.assertIsNone(data['current_category'])
    
    def test_search_question_no_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'this_is_a_very_long_string_that_is_definitely_not_in_the_database'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)
        self.assertIsNone(data['current_category'])

    def test_get_questions_by_category(self):
        category = 1
        res = self.client().get(f'/categories/{category}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['total_questions'], Question.query.filter(Question.category == 1).count())
        self.assertTrue(len(data['questions']) <= 10)
        self.assertEqual(data['current_category'], category)

        for question in data['questions']:
            self.assertEqual(question['category'], category)

    def test_get_questions_by_category_invalid_page(self):
        res = self.client().get('/categories/1/questions?page={}'.format(10000))
        data = json.loads(res.data)

        helper_error(self, res, data, 404)

    def test_generate_question_for_game_no_previous_any_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': {'type': 'click', 'id': 0}})
        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])

    def test_generate_question_for_game_specific_category(self):
        category = 1
        quiz_category = {'type': self.categories[str(category)], 'id': category}
        res = self.client().post('/quizzes', json={'previous_questions': [], 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertEqual(data['question']['category'], category)

    def test_generate_question_for_game_given_previous_questions(self):
        category = 1
        quiz_category = {'type': self.categories[str(category)], 'id': category}
        previous_questions = [20, 21] # Missing: 22
        res = self.client().post('/quizzes', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})
        data = json.loads(res.data)

        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['question'])
        self.assertEqual(data['question']['category'], category)
        self.assertEqual(data['question']['id'], 22)

    def test_generate_question_for_game_missing_body(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)

        helper_error(self, res, data, 400)

    def test_generate_question_for_game_missing_category(self):
        res = self.client().post('/quizzes', json={'previous_questions': []})
        data = json.loads(res.data)

        helper_error(self, res, data, 400)

    def test_generate_question_for_game_invalid_method(self):
        res = self.client().get('/quizzes')
        data = json.loads(res.data)

        helper_error(self, res, data, 405)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()