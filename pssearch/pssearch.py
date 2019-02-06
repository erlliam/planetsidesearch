import json
import urllib.request
from flask import Flask, render_template, request
app = Flask(__name__)

def get_character(name):
    character_id_url = "http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}".format(name.lower())
    character_id_result = urllib.request.urlopen(character_id_url).read()
    character_id_result = json.loads(character_id_result)
    if character_id_result['returned']:
        character_id_result = character_id_result['character_list'][0]
        username = character_id_result['name']['first']
        character_id = character_id_result['character_id']
        return [username, character_id]
    return False

def get_weapon_accuracy(character_id, item_id):
    weapon_url = "http://census.daybreakgames.com/s:supafarma/get/ps2/characters_weapon_stat/?character_id={}&item_id={}&stat_name=weapon_fire_count,weapon_hit_count&c:limit=2&c:show=value".format(character_id, item_id)
    weapon_result = urllib.request.urlopen(weapon_url).read()
    weapon_result = json.loads(weapon_result)
    weapon_result = int(weapon_result['characters_weapon_stat_list'][0]['value']) / int(weapon_result['characters_weapon_stat_list'][1]['value'])
    return weapon_result

@app.route('/')
def index():
    if 'user' in request.args:
        character_results = get_character(request.args['user'])
        if character_results:
            user = character_results[0]
            character_id = character_results[1]
            acc = get_weapon_accuracy(character_id, 80)
            return render_template('index.html', user=user, character_id=character_id, acc=acc)
        else:
            return render_template('index.html', status="usernotfound")
    return render_template('index.html')

