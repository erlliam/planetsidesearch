import urllib.request, json, sqlite3, os
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import char_search

app = Flask(__name__)
app.secret_key = "a"

def create_account(username, password):
    con = sqlite3.connect(os.path.join(app.root_path, 'static/accounts.db'))
    cur = con.cursor()
    cur.execute(""" INSERT INTO accounts ("username", "password")
            VALUES (?, ?)""", (username, generate_password_hash(password)))
    con.commit()
    con.close()

def check_account(username, password):
    con = sqlite3.connect(os.path.join(app.root_path, 'static/accounts.db'))
    cur = con.cursor()
    cur.execute(""" SELECT * FROM accounts WHERE
            "username"=?""", (username, ))
    account = cur.fetchone()
    con.close()

    if account and check_password_hash(account[2], password):
        return True
    else:
        return False

'static/accounts.db'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/character/')
def character():
    if 'name' in request.args:
        char = char_search.get_char_with_guns(request.args['name'])
        if char:
            return render_template('character.html', char=char)
    return render_template('character.html')

@app.route('/account/', methods=['GET'])
def account_get():
    return render_template('account.html')

@app.route('/account/', methods=['POST'])
def account_post():
    result = ''
    if 'sign-up' in request.form:
        try:
            create_account(request.form.get('sign-up-user'), request.form.get('sign-up-password'))
            session.update(user = request.form.get('sign-up-user'))
            result = 'account created, logged in'
        except sqlite3.IntegrityError:
            result = 'nametaken'
    elif 'log-in' in request.form:
        if check_account(request.form.get('log-in-user'), request.form.get('log-in-password')):
            session.update(user = request.form.get('log-in-user'))
        else:
            result = 'loginfail'
    elif 'log-out' in request.form:
        session.clear()
        result = 'loggedout'
    return render_template('account.html', result=result)

@app.route('/outfit/')
def outfit():
    return render_template('outfit.html')

@app.route('/elo/')
def elo():
    return render_template('elo.html')

if __name__ == '__main__':
    app.run(debug=True)
