# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


# Udacitrivia API Reference
The Udacitrivia API was built for the second project of Udacity's Full Stack Web Development Nanodegree. It powers a web-based trivia game, allowing users to browse through all trivia questions, filter them by a specific category, search for questions, add new questions, and play trivia games by pulling random non-repeated questions from all categories or from a specific category.

## Getting started
- Base URL: At present this API can only be run locally and is not hosted as a base URL. Thus, the base URL is `http://localhost:5000`.
- Authentication: This version of the application does not require authentication or API keys.

## Error handling
Errors are returned as JSON objects in the following format:
```json
{
    "success": false, 
    "error": 400,
    "message": "bad request"
}
```
The API will generally return four error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable
- 500: Internal Server Error


## Endpoints
### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: A JSON object with 2 keys: 
    - "categories": contains a object of id: category_string key:value pairs
    - "success": holds `true` if the request was successful
- Sample: `curl http://127.0.0.1:5000/categories`  
```json
200 OK
{
    "success": true,
    "categories": {
        "1" : "Science",
        "2" : "Art",
        "3" : "Geography",
        "4" : "History",
        "5" : "Entertainment",
        "6" : "Sports"
    }
}
```

### GET '/questions'
- Fetches a paginated list of questions objects, containing the question, answer, difficulty level, and category. By default, pages have at most 10 questions.
- Request arguments:
    - (Optional) `int page`: passed as a query parameter. If not provided, will be set as 1 by default.
- Returns: A JSON object with 5 keys:
    - "success": holds `true` if the request was successful
    - "questions": list of question objects for the given page
    - "total_questions": total number of questions in the database
    - "categories": object containing all categories in the database. Keys hold the category ID, value holds the category name
    - "current_category": null, since this call retrieves questions for all categories
- Sample: `curl http://127.0.0.1:5000/questions` or `curl http://127.0.0.1:5000/questions?page=1`
```json
200 OK
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography",
    "4": "History",
    "5": "Entertainment", 
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise", 
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3, 
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 18
}
```

### DELETE '/questions/{question_id}'
- Deletes a question from the database given the question ID
- Request arguments:
    - `int question_id`: passed as a path parameter, as seen in the request path
- Returns: A JSON object with 3 keys:
    - "success": holds `true` if the question was successfully deleted
    - "deleted": the id of the deleted question
    - "total_questions" the total number of questions after the deletion
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/28`
```json
200 OK
{
  "deleted": 28,
  "success": true,
  "total_questions": 17
}
```

### POST '/questions'
- Used for two separate resources, based on the provided body arguments:
1. Create new question
    - Inserts a new question into the database, given the question, answer, category, and difficulty
    - Request parameters (all required and passed as a JSON object as body arguments):
        - "question": a `string` that holds the trivia question
        - "answer": a `string` that holds the answer to the trivia question
        - "category": an `int` holding the ID of the question's category
        - "difficulty" an `int` in the range [1, 5] representing the difficulty of the question, if 5 being the most difficult
    - Returns: A JSON object with 3 keys:
        - "success": holds `true` if the question was successfully created
        - "created": the ID of the created question
        - "total_questions": the total number of questions after the insertion
    - Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"question": "Who is the 100-meter dash record holder?", "answer": "Usain Bolt", "category": 6, "difficulty": 2}'`
    ```json
    201 Created
    {
        "created": 29,
        "success": true,
        "total_questions": 18
    }
    ```
2. Search for a question
    - Searches for a question by case-insensitive partial string search
    - Request parameters:
        - "searchTerm": the `string` to be searched for (required and passed as a JSON object as body argument)
        - (Optional) `int page`: passed as a query parameter. If not provided, will be set as 1 by default.
    - Returns: A JSON object with 4 keys:
        - "success": holds `true` if the request was successful
        - "questions": the paginated result questions (at most 10 results per page)
        - "total_questions": the total number of results obtained from this search
        - "current_category": `null`, since the search doesn't account for specific categories
    - Sample: `curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d '{"searchTerm": "what"}'`
    ```json
    200 OK
    {
    "current_category": null,
    "questions": [
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
        "answer": "Tom Cruise",
        "category": 5,
        "difficulty": 4,
        "id": 4,
        "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
        "answer": "Muhammad Ali",
        "category": 4, 
        "difficulty": 1,
        "id": 9,
        "question": "What boxer's original name is Cassius Clay?"
        },
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
        },
        {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
        },
        {
        "answer": "Blood",
        "category": 1,
        "difficulty": 4,
        "id": 22,
        "question": "Hematology is a branch of medicine involving the study of what?"
        }
    ],
    "success": true,
    "total_questions": 8
    }
    ```

### GET '/categories/{category_id}/questions'
- Fetches questions based on a given category
- Request arguments:
    - `int category_id`: required and passed as a path parameter. Indicates the ID of the category whose questions we want to fetch
    - (Optional) `int page`: passed as a query parameter. If not provided, will be set as 1 by default.
- Returns: A JSON object with 4 keys:
    - "success": holds `true` if the request was successful
    - "questions": the questions for the given category
    - "total_questions": the total number of questions for the given category
    - "current_category": the ID of the category passed as a parameter
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
```json
200 OK
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
Alternatively, run 
```bash
bash run_tests.sh
```
from the backend directory.