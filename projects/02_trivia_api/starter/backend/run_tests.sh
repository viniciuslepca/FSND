dropdb -U postgres trivia_test
createdb -U postgres trivia_test
psql -U postgres trivia_test < trivia.psql
python3 test_flaskr.py