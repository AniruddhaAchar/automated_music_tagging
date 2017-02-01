import os

from flask import Flask, jsonify
from flask import flash
from flask import render_template
from flask import request
from flask_cors import CORS
from werkzeug.utils import secure_filename, redirect
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_restful import Api
from API.restful_api import FeaturedPlaylist, CategorySongs, SearchSongs
from Machine_Learning.audio_feature_extraction import get_audio_features
from cache_data import cache_featured_playlist, cache_category_songs, get_cache_featured_songs

app = Flask(__name__)
app.config.from_object('config')
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
scheduler = BackgroundScheduler()  # create a background scheduler task
scheduler.add_job(cache_featured_playlist, 'interval', minutes=50, id='store_playlist')  # add a job with target=
# cache_function, interval = 2 minutes
scheduler.add_job(cache_category_songs, 'interval', minutes=80, id='store_cat')
scheduler.start()  # start the scheduler

atexit.register(lambda: scheduler.shutdown())  # stop the scheduler when the server stops

api.add_resource(FeaturedPlaylist, '/api/v1.0/songs')
api.add_resource(CategorySongs, '/api/v1.0/cat/<string:category>')
api.add_resource(SearchSongs, '/api/v1.0/search')


@app.route('/')
def test():
    return render_template('index.html')





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
