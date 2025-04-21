from openai import AsyncOpenAI
from flask import Flask, request, jsonify
from quiz import Quiz
from database import initialize_database
from dotenv import load_dotenv
import os

# Initialize the Flask app
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client. If we want to use different clients for different API keys, do this in Quiz.py.
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Endpoint to initialize a SQLite database with necessary tables
@app.route('/create-database', methods=['POST'])
def create_db():
    initialize_database()
    return jsonify('Database created successfully')


# Endpoint to generate a quiz
@app.route('/generate-quiz', methods=['POST'])
async def create_quiz():
    '''
    Endpoint to generate a quiz


    Could generate a quiz ID, store the answers in sqlit, and return the quiz ID to the user for answer checking.
    Consider making quiz.py a class and store state in it.
    '''
    data = request.json
    topic = data['topic']
    num_questions = data['numq']
    question_type = data['qtype']
    quiz = Quiz(topic, question_type)

    # Generate Quiz
    try:
        quiz_data = await quiz.generate_quiz(num_questions, client)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify('quiz', quiz_data)


if __name__ == '__main__':
    app.run(debug=True)
