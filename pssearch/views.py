import urllib.request, json
from flask import Flask, render_template, request, session, redirect, url_for
import char_search, database

app = Flask(__name__)
app.secret_key = "a"

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

@app.route('/id_to_name')
def get_name():
    return char_search.id_to_name(request.args['id'])


@app.route('/account/', methods=['GET'])
def account_get():
    return render_template('account.html')

@app.route('/account/', methods=['POST'])
def account_post():
    result = ''
    if 'sign-up' in request.form:
        try:
            database.create_account(request.form.get('sign-up-user'), request.form.get('sign-up-password'))
            session.update(user = request.form.get('sign-up-user'))
            result = 'account created, logged in'
        except sqlite3.IntegrityError:
            result = 'nametaken'
    elif 'log-in' in request.form:
        if database.check_account(request.form.get('log-in-user'), request.form.get('log-in-password')):
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
