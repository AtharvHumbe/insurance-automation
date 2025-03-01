from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Function to create the SQLite database
def create_db():
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        print("Database and table created successfully.")
    except sqlite3.Error as e:
        print("Error creating database:", e)
    finally:
        conn.close()

# Call the function to create the database
create_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Change the hash method here

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
        conn.commit()
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        return "User with this email or username already exists"
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()

    if user and check_password_hash(user[3], password):
        return "Login successful"
    else:
        return "Invalid email or password"

if __name__ == '__main__':
    app.run(debug=True)
