from openai import AsyncOpenAI
from flask import Flask, request, jsonify
from quiz import get_previously_generated_questions, construct_prompt, generate_quiz, save_quiz 
from database import initialize_database

# Initialize the Flask app
app = Flask(__name__)

# Initialize the OpenAI client. If we want to use different clients for different API keys, do this in Quiz.py.
client = AsyncOpenAI()

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

    TODO: Add error handling. Store the quiz answers, so they can't be seen in dev tools. Add difficulty.
    Could generate a quiz ID, store the answers in sqlit, and return the quiz ID to the user for answer checking.
    Consider making quiz.py a class and store state in it.
    '''
    data = request.json
    topic = data['topic']
    num_questions = data['numq']
    question_type = data['qtype']
    previous_questions = get_previously_generated_questions(topic, question_type)
    
    # Construct Prompt
    prompt = construct_prompt(question_type, topic, num_questions, previous_questions)
    
    # Generate Quiz
    quiz_data = await generate_quiz(prompt, client)
    
    # Save Quiz to Database
    save_quiz(topic, quiz_data, question_type)
    
    return jsonify('quiz', quiz_data)


if __name__ == '__main__':
    app.run(debug=True)
