import sqlite3
import json
from database import DATABASE_NAME, SHORT_ANSWER_TABLE_NAME, MULTI_CHOICE_TABLE_NAME
from openai import AsyncOpenAI

'''
    Checks the database for existing questions of a given topic.

    @return: A string of previously generated questions for the given topic.
'''
# Fetches the previous questions for a given topic
def get_previously_generated_questions(topic: str, question_type:str) -> str:
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    if question_type == 'multi':
        cursor.execute(f'SELECT question FROM {MULTI_CHOICE_TABLE_NAME} WHERE topic = ?', (topic,))
    else:
        cursor.execute(f'SELECT question FROM {SHORT_ANSWER_TABLE_NAME} WHERE topic = ?', (topic,))
    previous_questions = cursor.fetchall()
    conn.close()

    # If there are no previous questions, return None
    if not previous_questions:
        return None
    return ' '.join(previous_questions)


"""
    Constructs a prompt for the OpenAI API based on the question type and topic.
"""
# TODO: Optimize prompts to minimize token usage.
def construct_prompt(question_type: str, topic: str, num_questions: int, previously_generated_questions: str) -> str:
    
    if question_type == 'multi':
        prompt = f"Create a multiple choice quiz on {topic} with {num_questions} questions. Each question should have 4 choices each consisting of 1 to 2 words. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'}"
    else:
        prompt = f"Create a quiz on {topic} with {num_questions} questions. Each question should have a 1 to 2 word solution. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'answer': 'Paris'}"
    prompt += f" Only include the JSON object in the response."
    if previously_generated_questions:
        prompt += f" Do not include questions similar to the following: {previously_generated_questions}"
    return prompt


'''
    Fetches the quiz data from the OpenAI API using the constructed prompt and omits previously generated questions.
'''
async def generate_quiz(prompt: str, client: AsyncOpenAI) -> dict:
    # Generate the quiz using OpenAI API
    response = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )

    # Extract the content from the response
    response_content = response.choices[0].message.content.strip()
    
    # Convert the JSON response to a dictionary and return
    quiz_data = json.loads(response_content.replace("'", '"'))
    return quiz_data


'''
    Saves the questions from a given quiz to the database.
'''
def save_quiz(topic, quiz_data, question_type):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    for question_data in quiz_data:
        try:
            if question_type == 'multi':
                cursor.execute(f'''
                    INSERT INTO {MULTI_CHOICE_TABLE_NAME} (question, type, topic, answer, option1, option2, option3, option4)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (question_data['question'], question_type, topic.lower(), question_data['answer'], question_data['option1'], question_data['option2'], question_data['option3'], question_data['option4']))
            else:
                cursor.execute(f'''
                    INSERT INTO {SHORT_ANSWER_TABLE_NAME} (question, type, topic, answer)
                    VALUES (?, ?, ?, ?)
                ''', (question_data['question'], question_type, topic.lower(), question_data['answer']))
        except sqlite3.IntegrityError:
            # Question already exists
            pass
    conn.commit()
    conn.close()