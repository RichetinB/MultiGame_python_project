from flask import Flask, render_template,request, redirect, url_for, session
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
    req = 'INSERT INTO users (username, password_hash, email) VALUES (?,?,?)'
    c.execute(req, (username, email, password_hash))
    c.commit()
    c.close()
    


@app.route('/')
def index():
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

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password_hash']
        
        conn = get_db_conection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password_hash = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = user['username']
            return redirect(url_for('index'))
        
        else:
            error_message = "Nom d'utilisateur ou mot de passe incorrect."
            return render_template('login.html', error_message=error_message)
    
    return render_template('login.html',error_message=None)

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
