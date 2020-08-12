import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_categories_object(categories):
  categories_object = {}
  for category in categories:
    categories_object[str(category.id)] = category.type
  return categories_object

def paginate_questions(questions, request):
  page = request.args.get('page', 1, type=int)
  start = (page-1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in questions]
  return formatted_questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r'/*': {'origins': '*'}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response


  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    categories_object = create_categories_object(categories)

    return jsonify({
      'success': True,
      'categories': categories_object
    })


  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    paginated_questions = paginate_questions(questions, request)

    if not paginated_questions and questions:
      abort(404)

    categories = Category.query.order_by(Category.id).all()
    categories_object = create_categories_object(categories)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(questions),
      'categories': categories_object,
      'current_category': None
    })

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    question = Question.query.filter(Question.id == id).one_or_none()
    if question is None:
      abort(404)

    question.delete()

    return jsonify({
      'success': True,
      'deleted': id,
      'total_questions': Question.query.count()
    })

  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()
    if body is None:
      abort(400)

    # Handle search
    search_term = body.get('searchTerm', None)
    if search_term is not None:
      results = Question.query.filter(Question.question.ilike('%' + search_term + '%')).order_by(Question.id).all()

      return jsonify({
        'success': True,
        'questions': paginate_questions(results, request),
        'total_questions': len(results),
        'current_category': None
      })

    # Handle create question
    question = body.get('question', None)
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)

    try:
      q = Question(question=question, answer=answer, category=category, difficulty=difficulty)
      q.insert()
    except:
      abort(422)
    finally:
      return jsonify({
        'success': True,
        'created': q.id,
        'total_questions': Question.query.count()
      }), 201


  '''
  @DONE: ABOVE
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    questions = Question.query.filter(Question.category == category_id).order_by(Question.id).all()
    paginated_questions = paginate_questions(questions, request)

    if not paginated_questions and questions:
      abort(404)

    return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(questions),
      'current_category': category_id
    })

  '''
  @DONE: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def generate_question_for_game():
    body = request.get_json()
    if body is None:
      abort(400)

    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', None)
    if quiz_category is None:
      abort(400)
    
    category_id = quiz_category.get('id', None)
    if category_id is None:
      abort(400)

    potential_questions = []
    if category_id == 0:   # Search for all categories
      potential_questions = Question.query.filter(~Question.id.in_(previous_questions)).all()
    else:
      potential_questions = Question.query.filter(~Question.id.in_(previous_questions), Question.category == category_id).all()
    
    if not potential_questions:
      return jsonify({
        'success': True,
        'question': None
      })

    question = random.choice(potential_questions)

    return jsonify({
      'success': True,
      'question': question.format()
    })

  '''
  @DONE: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable_entity(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable entity'
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal server error'
    }), 500
  
  return app

    