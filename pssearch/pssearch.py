import json
import urllib.request
from flask import Flask, render_template, request
app = Flask(__name__)

def get_character(name):
    character_id_url = "http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}".format(name.lower())
    character_id_result = urllib.request.urlopen(character_id_url)
    character_id_result = json.loads(character_id_result.read())
    if character_id_result['returned']:
        character_id_result = character_id_result['character_list'][0]
        username = character_id_result['name']['first']
        character_id = character_id_result['character_id']
        return [username, character_id]
    return False


@app.route('/')
def index():
    if 'user' in request.args:
        character_results = get_character(request.args['user'])
        if character_results:
            return render_template('index.html', user=character_results[0], character_id=character_results[1])
        else:
            return render_template('index.html', status="usernotfound")

    return render_template('index.html')

