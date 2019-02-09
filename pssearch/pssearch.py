import json
import pickle
import urllib.request
from flask import Flask, render_template, request
app = Flask(__name__)

items = open("pssearch/guns.pickle", "rb")
item_names = pickle.load(items)
items.close()

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

def get_name_from_id(item_id):
    if item_id in item_names:
        return item_names[item_id]
    return "notinlist"

def get_weapon_accuracy(character_id, item_id):
    weapon_url = "http://census.daybreakgames.com/s:supafarma/get/ps2/characters_weapon_stat/?character_id={}&item_id={}&stat_name=weapon_fire_count,weapon_hit_count&c:limit=2&c:show=value".format(character_id, item_id)
    weapon_result = urllib.request.urlopen(weapon_url).read()
    weapon_result = json.loads(weapon_result)
    weapon_result = int(weapon_result['characters_weapon_stat_list'][0]['value']) / int(weapon_result['characters_weapon_stat_list'][1]['value'])
    return weapon_result

def get_all_weapon_accuracy(name):
    all_wep_stats = "http://census.daybreakgames.com/get/ps2/characters_weapon_stat/?character_id={}&stat_name=weapon_fire_count,weapon_hit_count&vehicle_id=0&c:show=stat_name,item_id,value&c:limit=500".format(name.lower())
    all_wep_res = json.loads(urllib.request.urlopen(all_wep_stats).read())
    all_wep_res = all_wep_res['characters_weapon_stat_list']
    all_gun_acc = {}
    for value in all_wep_res:
        if value['stat_name'] == 'weapon_fire_count':
            all_gun_acc[value['item_id']] = [value['value']]
        else:
            if value['item_id'] in all_gun_acc:
                all_gun_acc[value['item_id']].append(value['value'])
    xd = {}
    for key, value in all_gun_acc.items():
        if len(value) == 2:
            xd[get_name_from_id(key)] = int(value[1])/int(value[0])
            
    return xd

@app.route('/')
def index():
    if 'user' in request.args:
        character_results = get_character(request.args['user'])
        if character_results:
            user, character_id = character_results
            get_all_weapon_accuracy(character_id)
            return render_template('index.html', user=user, character_id=character_id, gun_names=get_all_weapon_accuracy(character_id))
        else:
            return render_template('index.html', status="usernotfound")
    return render_template('index.html', gun_names=item_names)

