import json
import pickle
import urllib.request
from flask import Flask, render_template, request
app = Flask(__name__)

items = open("pssearch/guns.pickle", "rb")
item_names = pickle.load(items)
items.close()

def item_name(item_id):

    pass

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

def url_json(url):
    url_res = urllib.request.urlopen(url).read()
    json_res = json.loads(url_res)
    if json_res['returned']:
        return json_res
    else:
        return False

def search_character(name):
    url = "http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}".format(name.lower())
    json_res = url_json(url)
    if json_res:
        char_json = json_res['character_list'][0]
        return char_json['character_id'], char_json['name']['first']
    
def search_id(char_id):
    url = "http://census.daybreakgames.com/s:supafarma/get/ps2/character/?character_id={}".format(char_id)
    json_res = url_json(url)
    if json_res:
        char_json = json_res['character_list'][0]
        return char_json['character_id'], char_json['name']['first']

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' in request.args:
        char_res = search_character(request.args['user'])
        if char_res:
            char_id, user= char_res
            return render_template('index.html', user=user, char_id=char_id)
        else:
            return render_template('index.html', status="usernotfound")
    return render_template('index.html', gun_names=item_names)
