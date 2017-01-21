import os

from flask import Flask
from flask import flash
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename, redirect

app = Flask(__name__)
app.config.from_object('config')


@app.route('/')
def hello_world():
    return 'Hello World!'


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

            return "file saved successfully"
    if request.method == 'GET':
        return render_template('upload.html')


if __name__ == '__main__':
    app.run()
