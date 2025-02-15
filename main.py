from openai import AsyncOpenAI
import json
from flask import Flask, request, jsonify, render_template
import os
import sqlite3

# Initialize the Flask app
app = Flask(__name__)

# Initialize the OpenAI client
client = AsyncOpenAI()

# Function to generate a quiz
async def generate_quiz(topic, num_questions, qtype='single', previous_questions=None):
    # Construct the prompt based on the question type (short answer or multiple choice)
    if qtype == 'multi':
        # Multiple choice questions
        prompt = f"Create a multiple choice quiz on {topic} with {num_questions} questions. " + "Each question should have 4 choices each consisting of 1 to 2 words. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'}"
    else:
        prompt = f"Create a quiz on {topic} with {num_questions} questions. " + "Each questions should have a 1 to 2 word solution. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'answer': 'Paris'}"

    # Add additional instructions to the prompt
    prompt += f" Only include the JSON object in the response. Do not include any other text in the response."

    # Add previously generated questions to the prompt. 
    if previous_questions:
        prompt += f"Do not include the following questions in the quiz: {previous_questions}"

    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )

    response_content = response.choices[0].message.content.strip()
    quiz_data = json.loads(response_content.replace("'", '"'))

    # Convert the JSON response to a dictionary and return
    return quiz_data

# Fetches the previous questions for a given topic
def get_previous_questions(topic):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question FROM question WHERE topic = ?', (topic,))
    previous_questions = cursor.fetchall()
    conn.close()

    # If there are no previous questions, return None
    if not previous_questions:
        return None
    return previous_questions

# Saves the questions from a given quiz to the database
def save_quiz(topic, quiz_data, qtype):
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    for question_data in quiz_data:
        if qtype == 'single':
            option1 = None
            option2 = None
            option3 = None
            option4 = None
        else:
            option1 = quiz_data['choices'][0]
            option2 = quiz_data['choices'][1]
            option3 = quiz_data['choices'][2]
            option4 = quiz_data['choices'][3]
        try:
            cursor.execute('''
                INSERT INTO question (question, type, topic, answer, option1, option2, option3, option4)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (question_data['question'], qtype, topic, question_data['answer'], option1, option2, option3, option4))
        except sqlite3.IntegrityError:
            # Question already exists
            pass
    conn.commit()
    conn.close()

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
    qtype = data['type']
    previous_questions = get_previous_questions(topic)
    quiz_data = await generate_quiz(topic, num_questions, qtype, previous_questions)
    save_quiz(topic, quiz_data, qtype)
    return jsonify('quiz', quiz_data)

if __name__ == '__main__':
    app.run(debug=True)
