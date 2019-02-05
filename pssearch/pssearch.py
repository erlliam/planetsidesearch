import json
import urllib.request
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    if 'user' in request.args: 
        search = urllib.request.urlopen("http://census.daybreakgames.com/s:supafarma/get/ps2/character/?name.first_lower={}".format(request.args['user']))
        search = json.loads(search.read())
        if search['returned']:
            search = search['character_list'][0]
            user = search['name']['first']
            character_id = search['character_id']
            return render_template('index.html', user=user, character_id=character_id)

    return render_template('index.html')

