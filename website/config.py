import os

DEBUG = True
dir_path = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = dir_path+'\\website\\uploads\\music'
ALLOWED_EXTENSIONS = set(['mp3','wav'])
ROOT_ML = os.path.abspath(os.path.join(dir_path, os.pardir))
ROOT_CACHE = dir_path+'\\cache\\web'
