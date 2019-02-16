import urllib.request, json, sqlite3, os
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "a"

class Character:
    def __init__(self, c_id, name, fac):
        self.c_id = c_id
        self.name = name
        self.fac = fac

def url_json(url):
    url_res = urllib.request.urlopen(url).read()
    json_res = json.loads(url_res)
    if json_res['returned']:
        return json_res
    else:
        return False

def search_character(name):
    url = "http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}&c:join=faction^show:code_tag".format(name.lower())
    json_res = url_json(url)
    if json_res:
        char_json = json_res['character_list'][0]
        return Character(char_json['character_id'], char_json['name']['first'], char_json['faction_id_join_faction']['code_tag'])
    
def get_all_wep_acc(char_id):
    url = "http://census.daybreakgames.com/s:supafarma/get/ps2/characters_weapon_stat/?character_id={}&stat_name=weapon_fire_count,weapon_hit_count&vehicle_id=0&c:show=stat_name,item_id,value&c:limit=500&c:join=item^show:name.en".format(char_id)
    json_res = url_json(url)
    if json_res:
        wep_json = json_res['characters_weapon_stat_list']
        wep_dict = {}
        for wep in wep_json:
            item_id = wep['item_id']
            if not item_id in wep_dict:
                wep_dict[item_id] = [wep['item_id_join_item']['name']['en']]
            wep_dict[item_id].append(wep['value'])
        for key, value in list(wep_dict.items()):
            if len(value) != 3:
                del wep_dict[key]
        return wep_dict

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
    print(session)
    return render_template('index.html') 

@app.route('/character/')
def character():
    if 'name' in request.args:
        char_search = search_character(request.args.get('name'))
        if char_search:
            return render_template('character.html', char=char_search)
    return render_template('character.html')

@app.route('/account/', methods=['GET'])
def account_get():
    return render_template('account.html')

@app.route('/account/', methods=['POST'])
def account_post():
    if 'sign-up' in request.form:
        create_account(request.form.get('sign-up-user'), request.form.get('sign-up-password'))
        session.update(user = request.form.get('sign-up-user'))
    if 'log-in' in request.form:
        if check_account(request.form.get('log-in-user'), request.form.get('log-in-password')):
            session.update(user = request.form.get('log-in-user'))
    if 'log-out' in request.form:
        session.clear()
    return render_template('account.html')


'''

@app.route('/', methods=['POST'])
def index_post():
    if check_account(request.form.get('login-user'), request.form.get('login-password')):
        session.update(user = ((request.form.get('login-user')), request.form.get('login-password')))
        return redirect(request.referrer)
    else:
        return render_template('index.html', status='accountnotfoundorwrongpassword')

# temp
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(request.referrer)

@app.route('/signup', methods=['GET'])
def signup_get():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    create_account(request.form['user'], request.form['password'])
    return render_template('index.html')

'''
