import json
import os

from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename, redirect
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from API.spotify_API import get_featured_songs
from Machine_Learning.audio_feature_extraction import get_audio_features


app = Flask(__name__)
app.config.from_object('config')

scheduler = BackgroundScheduler()

global file_switch  # a variable used to switch between two different cache stored
file_switch = 0


def store_featured_playlist():
    global file_switch
    if 0 == file_switch:
        fs = 1
    else:
        fs = 0
    print(fs, file_switch)
    featured = get_featured_songs()
    js = json.dumps(featured)
    if os.path.isfile(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json'):
        with open(app.config['UPLOAD_FOLDER'] + 'featured_playlist{}.json'.format(fs), 'r') as fread:
            if js == fread.read():
                return
    with open(app.config['UPLOAD_FOLDER'] + 'featured_playlist{}.json'.format(fs), 'w') as fpfile:
        fpfile.write(js)
        file_switch = fs

scheduler.add_job(store_featured_playlist, 'interval', minutes=2, id='store_playlist')
scheduler.start()

atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def index():
    if not os.path.isfile(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json'):
        print("File not exists")
        store_featured_playlist()
        with open(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json') as songs:
            return songs.read()
    if os.path.getsize(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json') <= 0:
        print("File size zero")
        store_featured_playlist()
        with open(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json') as songs:
            return songs.read()
    with open(app.config['UPLOAD_FOLDER'] + 'featured_playlist' + str(file_switch) + '.json') as songs:
        return songs.read()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['music']
        if file.filename == "":
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "file saved successfully " + get_audio_features(filename)
    if request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
