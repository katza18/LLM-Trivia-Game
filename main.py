from openai import AsyncOpenAI
from flask import Flask, request, jsonify, render_template
import sqlite3
from quiz import get_previously_generated_questions, construct_prompt, generate_quiz, save_quiz

# Initialize the Flask app
app = Flask(__name__)

# Initialize the OpenAI client. If we want to use different clients for different API keys, do this in Quiz.py.
client = AsyncOpenAI()

# Endpoint to initialize a SQLite database
@app.route('/create-database', methods=['POST'])
def init_db():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY,
            question TEXT,
            type TEXT,
            topic TEXT,
            answer TEXT,
            option1 TEXT,
            option2 TEXT,
            option3 TEXT,
            option4 TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Endpoint to generate a quiz
@app.route('/generate-quiz', methods=['POST'])
async def quiz():
    '''
    Endpoint to generate a quiz

    TODO: Add error handling. Store the quiz answers, so they can't be seen in dev tools. Add difficulty.
    Could generate a quiz ID, store the answers in sqlit, and return the quiz ID to the user for answer checking.
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
