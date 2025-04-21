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


if __name__ == '__main__':
    app.run(debug=True)
