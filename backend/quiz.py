from backend.db.database import DATABASE_NAME, SHORT_ANSWER_TABLE_NAME, MULTI_CHOICE_TABLE_NAME
from openai import AsyncOpenAI
from backend.crud.question import get_previous_questions, save_quiz
from pydantic import BaseModel
from backend.crud.user import get_user
import tiktoken

class QuizRequest(BaseModel):
    topic: str
    qtype: str
    numq: int


"""
    Constructs a prompt for the OpenAI API based on the question type and topic.
"""
# TODO: Optimize prompts to minimize token usage.
def construct_prompt(quiz_params: QuizRequest) -> str:
    # Get previously generated questions
    previously_generated_questions = get_previous_questions()

    # Construct the prompt based on the question type
    if quiz_params.qtype == 'multi':
        prompt = f"Create a multiple choice quiz on {quiz_params.topic} with {quiz_params.numq} questions. Each question should have 4 choices each consisting of 1 to 2 words. Format the output as JSON with the following structure: {{'question': 'What is the capital of France?', 'choices': ['Paris', 'London', 'Berlin', 'Madrid'], 'answer': 'Paris'}}"
    else:
        prompt = f"Create a quiz on {quiz_params.topic} with {quiz_params.numq} questions. Each question should have a 1 to 2 word solution. Format the output as JSON with the following structure: {{'question': 'What is the capital of France?', 'answer': 'Paris'}}"
    prompt += f" Only include the JSON object in the response."
    if previously_generated_questions:
        prompt += f" Do not include questions similar to the following: {previously_generated_questions}"
    return prompt


def is_allowed_to_generate_quiz(user_id: str, prompt: str) -> bool:
    '''
    Check if the user has enough quota to generate a quiz.
    This function should check the user's quota and return True or False.
    '''
    # Get the user's quota and used tokens
    encoding = tiktoken.encoding_for_model("gpt-4o-mini")

    try:
        user = get_user(user_id)
        quota = user.quota
        used = user.token_used
        prompt_tokens = encoding.encode(prompt)
        # Check if the user has enough quota
        if quota - used - prompt_tokens > 0:
            return True
        return False
    except Exception as e:
        return False


'''
    Fetches the quiz data from the OpenAI API using the constructed prompt and omits previously generated questions.
'''
async def generate_quiz(quiz_params: QuizRequest, client: AsyncOpenAI, user_id: str) -> dict:
    # Create the prompt
    prompt = construct_prompt(quiz_params)

    # Check user's quota
    if not is_allowed_to_generate_quiz(user_id, prompt):
        raise Exception("User has exceeded their quota for generating quizzes.")

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

        # Strip the response of any preceding or trailing formatting characters
        quiz_data = strip_response_formatting(response_content.replace("'", '"'))

        # Pass json quiz_data to crud function. FastAPI and pydantic will handle the conversion to a dict.
        save_quiz(quiz_data)

        return quiz_data
    except Exception as e:
        raise e


def strip_response_formatting(response_content) -> str:
    '''
    Strips the prompt of any preceding or trailing formatting characters. String should start with [ and end with ]
    '''
    # Remove leading and trailing whitespace and brackets
    if not response_content.startswith("["):
        while len(response_content) > 0 and response_content[0] != "[":
            response_content = response_content[1:]
    if not response_content.endswith("]"):
        while len(response_content) > 0 and response_content[-1] != "]":
            response_content = response_content[:-1]
    return response_content
