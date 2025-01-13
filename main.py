import openai
import json
from flask import Flask, request, jsonify

def generate_quiz(topic, num_questions, qtype='single'):
    if type == 'multi':
        # Multiple choice questions
        prompt = f"Create a multiple choice quiz on {topic} with {num_questions} questions. " + "Each question should have 4 choices each consisting of 1 to 2 words. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'}"
    else:
        prompt = f"Create a quiz on {topic} with {num_questions} questions. " + "Each questions should have a 1 to 2 word solution. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'answer': 'Paris'}"


    prompt += " Only include the JSON object in the response. Do not include any other text in the response."

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=200
    )

    # Convert the JSON response to a dictionary and return
    return json.loads(response.choices[0].text.strip())

app = Flask(__name__)

@app.route('/generate-quiz', methods=['POST'])
def quiz():
    '''
    Endpoint to generate a quiz

    TODO: Add error handling. Store the quiz answers, so they can't be seen in dev tools.
    Could generate a quiz ID, store the answers in sqlit, and return the quiz ID to the user for answer checking.
    '''
    data = request.json
    topic = data['topic']
    num_questions = data['numq']
    qtype = data['type']
    quiz_data = generate_quiz(topic, num_questions, qtype)
    return jsonify('quiz', quiz_data)

@app.route('/save-progress', methods=['POST'])
def save():
    '''
    Endpoint to save the user's progress
    '''
    data = request.json
    # Save the user's progress
    return jsonify('status': 'progress saved')