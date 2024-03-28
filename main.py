from flask import Flask, render_template,request, redirect, url_for, session, jsonify

import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'Baptiste-31052004'


def get_db_conection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def add_user(username, email, password_hash):
    c = get_db_conection()
    req = 'INSERT INTO users (username, email, password_hash) VALUES (?,?,?)'
    c.execute(req, (username, email, password_hash))
    c.commit()
    c.close()   
    
def get_user(username, password_hash):
    conn = get_db_conection()
    user = conn.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password_hash)).fetchone()
    conn.close()
    return user



@app.route('/send_message', methods=['POST'])
def send_message():
    if request.method == 'POST':
        sender_id = request.form['sender_id']
        # receiver_id = request.form['receiver_id']
        content = request.form['content']

        conn = get_db_conection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (sender_id, content) VALUES (?, ?)", (sender_id, content))
        conn.commit()
        conn.close()

        return redirect(url_for('view_messages'))


@app.route('/messages')
def view_messages():
    conn = get_db_conection()
    cursor = conn.cursor()
    messages = cursor.execute("SELECT * FROM messages").fetchall()
    conn.close()

    return render_template('index.html', messages=messages)


@app.route('/')
def index():
    # if 'username' in session:
    #     return f'Bienvenue, {session["username"]}! <a href="/logout">Se déconnecter</a>'
    # else:
    conn = get_db_conection()
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user_route():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_hash = request.form['password_hash']
        add_user(username, email, password_hash)
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = get_user(username, password)
        
        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html', error_message=None)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/lol_valo')
def lol_valo():
    valo_ou_lol = ["valo", "lol"]
    jeu = random.choice(valo_ou_lol)
    return f"Je vais jouer à {jeu}"

if __name__ == '__main__':
    app.run(debug=True)
