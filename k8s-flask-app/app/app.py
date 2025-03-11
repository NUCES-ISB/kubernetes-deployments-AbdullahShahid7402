from flask import Flask, request, render_template_string, redirect, url_for
import psycopg2
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get('POSTGRES_DB', 'mydatabase'),
            user=os.environ.get('POSTGRES_USER', 'user'),
            password=os.environ.get('POSTGRES_PASSWORD', 'password'),
            host='postgres'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create table if it doesn't exist
def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            roll_number VARCHAR(100)
        )
    ''')
    conn.commit()
    cur.close()
    conn.close()

create_table()

# HTML template
html_template = '''
    <h1>Student Registration</h1>
    <form method="POST" action="/">
        Name: <input type="text" name="name"><br>
        Roll Number: <input type="text" name="roll_number"><br>
        <input type="submit" value="Add Student">
    </form>
    <h2>Current Students</h2>
    <ul>
    {% for student in students %}
        <li>{{ student[1] }} (Roll Number: {{ student[2] }})</li>
    {% endfor %}
    </ul>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        cur.execute('INSERT INTO students (name, roll_number) VALUES (%s, %s)', (name, roll_number))
        conn.commit()

    cur.execute('SELECT * FROM students')
    students = cur.fetchall()
    cur.close()
    conn.close()

    return render_template_string(html_template, students=students)

@app.route('/')
def check_db_connection():
    conn = get_db_connection()
    if conn:
        conn.close()
        return '''
            <h1>Connected to the PostgreSQL database successfully!</h1>
            <form action="/insert" method="post">
                <input type="submit" value="Add Student">
            </form>
        '''
    else:
        return "Failed to connect to the PostgreSQL database."

@app.route('/insert', methods=['POST'])
def insert_data():
    # Simulate data insertion
    # In a real application, you would insert data into the database here
    return redirect(url_for('insertion_successful'))

@app.route('/insertion-successful')
def insertion_successful():
    return '''
        <h1>Insertion Successful!</h1>
        <a href="/">Go back to Home</a>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0')