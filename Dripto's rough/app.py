from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="directrix",
    user="postgres",
    password="dripzapy",
    port="5433"
)
cur = conn.cursor()

# create a table for storing user information
cur.execute('''CREATE TABLE IF NOT EXISTS users 
             (id SERIAL PRIMARY KEY,
              username TEXT,
              password TEXT)''')
conn.commit()

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # check if the user exists in the database
        cur.execute('SELECT * FROM users WHERE username=%s AND password=%s', 
                  (username, password))
        users = cur.fetchall()
        
        if users:
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
        
    return render_template('login.html')

# sign up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # check if the username already exists in the database
        cur.execute('SELECT * FROM users WHERE username=%s', (username,))
        user = cur.fetchone()
        
        if user:
            return render_template('signup.html', error='Username already taken')
        else:
            # add the new user to the database
            cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', 
                      (username, password))
            conn.commit()
            return redirect(url_for('home'))
        
    return render_template('signup.html')

# home page
@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)