import os
import json
from pprint import pprint
from flask import Flask, jsonify
from flask import flash
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename, redirect
from Machine_Learning.audio_feature_extraction import get_audio_features
from API.spotify_API import get_featured_songs, search_song


app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def indexpage():
    t_songs = get_featured_songs()
    return render_template('indexpage.html', t_songs=t_songs)


@app.route('/search', methods=['GET', 'POST'])
def searchpage():
    if request.method == 'GET':
        return render_template("searchpage.html")


@app.route('/background')
def background():
    s_str = request.args.get('searchstr')
    s_res = search_song(str(s_str))
    print(s_str)
    pprint(s_res)
    return jsonify(result=s_res)


@app.route('/activity')
def activitypage():
    activty_list = ['workout', 'party', 'sleep', 'dinner']
    ftsongs = get_featured_songs()

    return render_template('activity_based.html', ftsongs=ftsongs, activity_list=activty_list)


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
            return "file saved successfully" + get_audio_features(filename)
    if request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
