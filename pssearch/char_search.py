import urllib.request, json

url = """http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}&c:show=character_id,name.first,faction_id,times.minutes_played,battle_rank.value,prestige_level&c:join=faction^inject_at:faction_id^show:code_tag&c:join=characters_weapon_stat^inject_at:wep_acc^terms:vehicle_id=0%27stat_name=weapon_deaths%27stat_name=weapon_fire_count%27stat_name=weapon_hit_count^show:item_id%27stat_name%27value^list:1^outer:0(item^show:name.en^inject_at:gun_name)&c:tree=start:wep_acc^field:item_id,stat_name^list:1&c:join=characters_weapon_stat_by_faction^inject_at:wep_kill^terms:vehicle_id=0%27stat_name=weapon_headshots%27stat_name=weapon_kills^show:item_id%27stat_name%27value_vs%27value_nc%27value_tr^list:1(item^show:name.en^inject_at:gun_name)&c:tree=start:wep_kill^field:item_id,stat_name^list:1"""

"""
u = url
j = json
r = access data
k = weapon kills, weapon headshots, located where injected
a = weapon accuracy, deaths, location where injected
f = final dict, remove incomplete items(must have all 5 stats, weapon: kills, deaths, hit, fired, headshots)
g = gun list with 

create character with stuff and gun list
"""

class Character:
    def __init__(self, cid, name, fac, time, rank, pres):
        self.cid = cid
        self.name = name
        self.fac = fac
        self.time = time
        self.rank = rank
        self.pres = pres

    def set_guns(self, guns):
        self.guns = guns

class Gun:
    def __init__(self, d):
        self.d = d
        self.item_id = list(d.keys())[0]
        self.name = d['name']
        self.kills = d['weapon_kills']
        self.headshots = d['weapon_headshots']
        self.deaths = d['weapon_deaths']
        self.fired = d['weapon_fire_count']
        self.landed = d['weapon_hit_count']

def get_char(name):
    u = urllib.request.urlopen(url.format(name.lower()))
    j = json.load(u)
    if not j['returned']:
        return False
    r = j['character_list'][0]

    c = Character(
            r['character_id'],
            r['name']['first'],
            r['faction_id']['code_tag'],
            r['times']['minutes_played'],
            r['battle_rank']['value'],
            r['prestige_level']
            )

    return c


def get_char_with_guns(name):
    u = urllib.request.urlopen(url.format(name.lower()))
    j = json.load(u)

    if not j['returned']:
        return False
    elif not len(j['character_list']):
        return False
    print(j)
    r = j['character_list'][0]

    if not 'wep_kill' in r or not 'wep_acc' in r:
        return False # fixes if gun is shot and no bullets landed??
    k = r['wep_kill']
    a = r['wep_acc']

    c = Character(
            r['character_id'],
            r['name']['first'],
            r['faction_id']['code_tag'],
            r['times']['minutes_played'],
            r['battle_rank']['value'],
            r['prestige_level']
            )

    f = {}

    for item_id, values in k.items():
        if not item_id in f:
            f[item_id] = {}
        for stat_name, result in values.items():
            final_val = 0
            for i, v in result[0].items():
                if isinstance(v, str):
                    final_val = final_val + int(v)
            if not 'name' in f[item_id]:
                f[item_id]['name'] = result[0]['gun_name']['name']['en']
            f[item_id].update({stat_name: final_val})

    for item_id, values in a.items():
        if not item_id in f:
            f[item_id] = {}
        for stat_name, result in values.items():
            if not 'name' in f[item_id]:
                f[item_id]['name'] = result[0]['gun_name']['name']['en']
            f[item_id].update({stat_name: result[0]['value']})

    for i, v in f.copy().items():
        if not len(v) == 6:
            del f[i]

    g = []

    for i, v in f.items():
        g.append(Gun(v))

    c.set_guns(g)
    return c


