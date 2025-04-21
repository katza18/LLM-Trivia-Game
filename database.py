import sqlite3

DATABASE_NAME = 'quiz.db'
SHORT_ANSWER_TABLE_NAME = 'short_answer_question'
MULTI_CHOICE_TABLE_NAME = 'multiple_choice_question'

def initialize_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {MULTI_CHOICE_TABLE_NAME} (
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
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {SHORT_ANSWER_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            question TEXT,
            type TEXT,
            topic TEXT,
            answer TEXT
        )
    ''')
    conn.commit()
    conn.close()


def get_answer(question_id: str, question_type: str) -> str:
        # Check the answer in the database
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        if question_type == 'multi':
            table_name = MULTI_CHOICE_TABLE_NAME
        else:
            table_name = SHORT_ANSWER_TABLE_NAME
        
        cursor.execute(f'SELECT answer FROM {table_name} WHERE id=?', (question_id,))
        correct_answer = cursor.fetchone()

        if correct_answer:
            correct_answer = correct_answer[0]
            return correct_answer
        else:
            return None