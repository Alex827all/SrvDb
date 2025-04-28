from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Функция для подключения к БД
def connect_db():
    conn = sqlite3.connect('form_data.db')
    return conn

# Создание таблицы
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Главная страница с формой
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        message = request.form['message']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO submissions (name, message) VALUES (?, ?)
        ''', (name, message))
        conn.commit()
        conn.close()

        return "Данные успешно сохранены!"

    return render_template('index.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
