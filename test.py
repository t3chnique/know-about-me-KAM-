import uuid
import sqlite3
import json

unqie_code = str(uuid.uuid4())
database_name = f'user_profile({unqie_code}).db'


def create_table():
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_answer_to_db(question, answer):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute('''
        INSERT INTO profile (question, answer) VALUES (?, ?)
    ''', (question, answer))
    conn.commit()
    conn.close()


def load_questions():
    with open('questions.json', 'r') as file:
        data = json.load(file)
    return data['questions']


def ask_questions(questions):
    for i, question in enumerate(questions, 1):
        answer = input(f"{i}. {question} ")
        save_answer_to_db(question, answer)


def read_database(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute('SELECT question, answer FROM profile')
    rows = c.fetchall()
    conn.close()
    return rows


def generate_txt_file(data, output_file=f'{database_name}.txt'):
    with open(output_file, 'w') as file:
        for question, answer in data:
            file.write(f"Question: {question}\nAnswer: {answer}\n\n")


if __name__ == "__main__":
    action = input("Do you want to read an existing database file or "
                   "create a new profile? (read/create): ").strip().lower()
    if action == 'read':
        filename = input("Enter the name of the SQLite database "
                         "file to read (e.g., 'profile.db'): ")
        data = read_database(filename)
        generate_txt_file(data)
        print(f"\nData from {filename} has been written "
              "to 'profile_output.txt'.")
    elif action == 'create':
        create_table()
        questions = load_questions()
        ask_questions(questions)
        print("\nThank you for sharing! "
              "Your profile has been saved to the database.")
        filename = database_name
        data = read_database(filename)
        generate_txt_file(data, output_file=f'{database_name}.txt')
    else:
        print("Invalid option. "
              "Please restart the program "
              "and choose either 'read' or 'create'.")
