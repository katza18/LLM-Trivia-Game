from openai import AsyncOpenAI
from flask import Flask, request, jsonify
from flask_cors import CORS
from quiz import Quiz
from database import initialize_database, get_answer
from dotenv import load_dotenv
import os

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client. If we want to use different clients for different API keys, do this in Quiz.py.
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# TODO: Remove in production.
@app.route('/create-database', methods=['POST'])
def create_db():
    '''
    Endpoint to create a SQLite database with necessary tables.
    '''
    initialize_database()
    return jsonify('Database created successfully')


@app.route('/generate-quiz', methods=['POST'])
async def create_quiz():
    '''
    Endpoint to generate a quiz


    Could generate a quiz ID, store the answers in sqlit, and return the quiz ID to the user for answer checking.
    Consider making quiz.py a class and store state in it.
    '''
    data = request.json
    quiz = Quiz(data['topic'], data['qtype'])

    # Generate Quiz
    try:
        quiz_data = await quiz.generate_quiz(data['numq'], client)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'quiz': quiz_data})


@app.route('/check-answer', methods=['POST'])
def check_answer():
    '''
    Endpoint to check the answer of a quiz question.
    '''
    data = request.json

    try:
        correct_answer = get_answer(data['qid'], data['qtype'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'correct_answer': correct_answer})


@app.route('/questions/favorites', methods=['GET'])
def get_favorite_questions():
    '''
    Endpoint to get all favorite questions from the database.
    '''

    data = request.json
    question_type = data['type']
    page = data['page']
    page_size = data['page_size']

    try:
        favorite_questions = get_favorites()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'favorite_questions': favorite_questions})


@app.route('/questions/<int:qid>/favorite', methods=['POST, DELETE'])
def favorite_question(qid):
    '''
    Endpoint to favorite or unfavorite a question.
    '''
    action = request.method

    try:
        if action == 'POST':
            add_to_favorites(qid)
        elif action == 'DELETE':
            remove_from_favorites(qid)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'Question {action}d successfully'})



@app.route('/lists', methods=['GET'])
def get_lists():
    '''
    Endpoint to get all lists from the database.
    '''
    data = request.json
    user = data['user']
    page = data['page']
    page_size = data['page_size']

    try:
        lists = get_all_lists()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'lists': lists})


@app.route('/user/usage', methods=['GET'])
def get_user_usage():
    '''
    Endpoint to get user usage statistics.
    '''
    data = request.json
    user = data['user']

    try:
        usage = get_user_statistics(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'usage': usage})


@app.route('auth/login', methods=['POST'])
def login():
    '''
    Endpoint to log in a user.
    '''
    data = request.json
    username = data['username']
    password = data['password']

    try:
        user = authenticate_user(username, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'user': user})


@app.route('/auth/signup', methods=['POST'])
def signup():
    '''
    Endpoint to register a new user.
    '''
    data = request.json
    username = data['username']
    password = data['password']

    try:
        user = register_user(username, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'user': user})


@app.route('/auth/logout', methods=['POST'])
def logout():
    '''
    Endpoint to log out a user.
    '''
    data = request.json
    user = data['user']

    try:
        logout_user(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'User logged out successfully'})


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    '''
    Endpoint to reset a user's password.
    '''
    data = request.json
    username = data['username']
    new_password = data['new_password']

    try:
        reset_user_password(username, new_password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Password reset successfully'})


if __name__ == '__main__':
    app.run(debug=True)
