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

scheduler = BackgroundScheduler()  # create a background scheduler task


def cache_featured_playlist():
    """
    This function caches the featured playlist. If there are any changes between the current version and the previous
    version, the file is updated.
    :return: None
    """
    featured = get_featured_songs()
    js = json.dumps(featured)
    if os.path.isfile(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json'):  # check if file exists
        with open(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json', 'r') as fread:  # get the file where the
            # cache is stored
            if js == fread.read():  # if new data and cache are same, do nothing
                return
    with open(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json', 'w') as fpfile:  # else update the file
        fpfile.truncate()
        fpfile.write(js)


scheduler.add_job(cache_featured_playlist, 'interval', minutes=2, id='store_playlist')  # add a job with target=
# cache_function, interval = 2 minutes
scheduler.start()  # start the scheduler

atexit.register(lambda: scheduler.shutdown())  # stop the scheduler when the server stops


@app.route('/')
def index():
    if not os.path.isfile(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json'):
        cache_featured_playlist()
        with open(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json') as songs:
            return songs.read()
    if os.path.getsize(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json') <= 0:
        cache_featured_playlist()
        with open(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json') as songs:
            return songs.read()
    with open(app.config['UPLOAD_FOLDER'] + '\\featured_playlist.json') as songs:
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
