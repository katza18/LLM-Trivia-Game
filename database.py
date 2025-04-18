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
            answer TEXT,
        )
    ''')
    conn.commit()
    conn.close()