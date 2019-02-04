from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    if 'user' in request.args: 
        return render_template('index.html', user=request.args['user'])

    return render_template('index.html')

