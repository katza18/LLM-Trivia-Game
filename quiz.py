import sqlite3
import json
from database import DATABASE_NAME, SHORT_ANSWER_TABLE_NAME, MULTI_CHOICE_TABLE_NAME
from openai import AsyncOpenAI

class Quiz:
    '''
        Quiz class to handle quiz generation and database interactions.
        TODO: Add difficulty.
    '''
    def __init__(self, topic: str, question_type: str):
        '''
            Initializes the Quiz class with the OpenAI client, topic, and question type.

            @param client: The OpenAI client to use for generating quizzes.
            @param topic: The topic for the quiz.
            @param question_type: The type of questions to generate (multiple choice or short answer).
        '''
        self.topic = topic.lower()
        self.question_type = question_type

    
    '''
        Checks the database for existing questions of a given topic.

        @return: A string of previously generated questions for the given topic.
    '''
    # Fetches the previous questions for a given topic
    def get_previously_generated_questions(self) -> str:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        # Determine the table name based on the question type
        table_name = MULTI_CHOICE_TABLE_NAME if self.question_type == 'multi' else SHORT_ANSWER_TABLE_NAME
        
        # Fetch the previous questions from the database
        cursor.execute(f'SELECT question FROM {table_name} WHERE topic = ?', (self.topic,))
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
    def construct_prompt(self, num_questions: str) -> str:
        # Get previously generated questions
        previously_generated_questions = self.get_previously_generated_questions()
        
        # Construct the prompt based on the question type
        if self.question_type == 'multi':
            prompt = f"Create a multiple choice quiz on {self.topic} with {num_questions} questions. Each question should have 4 choices each consisting of 1 to 2 words. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'}"
        else:
            prompt = f"Create a quiz on {self.topic} with {num_questions} questions. Each question should have a 1 to 2 word solution. Format the output as JSON with the following structure: {'question': 'What is the capital of France?', 'answer': 'Paris'}"
        prompt += f" Only include the JSON object in the response."
        if previously_generated_questions:
            prompt += f" Do not include questions similar to the following: {previously_generated_questions}"
        return prompt


    '''
        Fetches the quiz data from the OpenAI API using the constructed prompt and omits previously generated questions.
    '''
    async def generate_quiz(self, num_questions: str, client: AsyncOpenAI) -> dict:
        # Create the prompt
        prompt = self.construct_prompt(num_questions)

        # Generate the quiz using OpenAI API
        try:
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

            # Save the quiz data to the database
            self.save_quiz(quiz_data, self.question_type, self.topic)

            return quiz_data
        except Exception as e:
            raise e


    '''
    Inserts a question into the database.
    '''
    def save_question(self, cursor, question_data):
        try:
            if self.question_type == 'multi':
                cursor.execute(f'''
                    INSERT INTO {MULTI_CHOICE_TABLE_NAME} (question, type, topic, answer, option1, option2, option3, option4)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (question_data['question'], self.question_type, self.topic, question_data['answer'], question_data['option1'], question_data['option2'], question_data['option3'], question_data['option4']))
            else:
                cursor.execute(f'''
                    INSERT INTO {SHORT_ANSWER_TABLE_NAME} (question, type, topic, answer)
                    VALUES (?, ?, ?, ?)
                ''', (question_data['question'], self.question_type, self.topic, question_data['answer']))
        except sqlite3.IntegrityError:
            # Question already exists
            pass


    '''
        Saves the questions from a given quiz to the database.
    '''
    def save_quiz(self, quiz_data):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        for question_data in quiz_data:
            self.save_question(cursor, question_data, self.question_type, self.topic)
        conn.commit()
        conn.close()