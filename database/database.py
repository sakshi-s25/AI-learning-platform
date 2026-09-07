import sqlite3

DATABASE_NAME = "learning_platform.db"

def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection

def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL, password TEXT NOT NULL, skills TEXT, learning_goal TEXT, study_time INTEGER DEFAULT O)""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS assessment_results ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, score INTEGER, total_questions INTEGER, FOREIGN KEY (user_id) REFERENCES users(id))""")

    connection.commit()
    connection.close()

