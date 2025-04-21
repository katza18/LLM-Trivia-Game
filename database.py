import sqlite3

DATABASE_NAME = 'quiz.db'
SHORT_ANSWER_TABLE_NAME = 'short_answer_question'
MULTI_CHOICE_TABLE_NAME = 'multiple_choice_question'
USER_TABLE_NAME = 'user'
USER_QUESTION_VIEW_TABLE_NAME = 'user_question_view'
QUESTION_LIST_TABLE_NAME = 'question_list'
QUESTION_LIST_ITEM_TABLE_NAME = 'question_list_item'
TOKEN_LOG_TABLE_NAME = 'token_log'

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
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {USER_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            tier TEXT DEFAULT 'free',
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            token_quota INTEGER DEFAULT 1000,
            token_used INTEGER DEFAULT 0,
            token_expiry TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            stripe_customer_id TEXT
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {USER_QUESTION_VIEW_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            question_id INTEGER,
            question_type TEXT,
            view_count INTEGER DEFAULT 1,
            last_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES {USER_TABLE_NAME}(id),
            FOREIGN KEY (question_id) REFERENCES {MULTI_CHOICE_TABLE_NAME}(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {QUESTION_LIST_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            NAME TEXT,
            FOREIGN KEY (user_id) REFERENCES {USER_TABLE_NAME}(id),
            FOREIGN KEY (question_id) REFERENCES {MULTI_CHOICE_TABLE_NAME}(id)
        )
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {QUESTION_LIST_ITEM_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            question_list_id INTEGER,
            question_id INTEGER,
            question_type TEXT,
            FOREIGN KEY (question_list_id) REFERENCES {QUESTION_LIST_TABLE_NAME}(id),
            FOREIGN KEY (question_id) REFERENCES {MULTI_CHOICE_TABLE_NAME}(id)
        )               
    ''')
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TOKEN_LOG_TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            tokens_used INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES {USER_TABLE_NAME}(id)
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