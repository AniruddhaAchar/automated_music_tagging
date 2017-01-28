import json
import os

from API.spotify_API import get_category_songs, get_featured_songs
from config import ROOT_CACHE


def cache_featured_playlist():
    """
    This function caches the featured playlist. If there are any changes between the current version and the previous
    version, the file is updated.
    :return: None
    """
    featured = get_featured_songs()
    js = featured
    save_cache(js, 'featured_playlist.json')


def save_cache(data, file_name):
    if os.path.isfile(ROOT_CACHE + '\\' + file_name):  # check if file exists
        with open(ROOT_CACHE + '\\' + file_name, 'r') as fread:  # get the file where the
            # cache is stored
            if data == fread.read():  # if new data and cache are same, do nothing
                return
    with open(ROOT_CACHE + '\\' + file_name, 'w') as fpfile:  # else update the file
        print("Cleaning data")
        fpfile.seek(0)
        fpfile.truncate()
        fpfile.seek(0, 2)
        print(fpfile.tell())
        fpfile.seek(0)
        fpfile.write(data)


def cache_category_songs():
    party = get_category_songs('party')
    sleep = get_category_songs('sleep')
    workout = get_category_songs('workout')
    dinner = get_category_songs('dinner')
    save_cache(party, 'party_songs.json')
    save_cache(sleep, 'sleep_songs.json')
    save_cache(workout, 'workout_songs.json')
    save_cache(dinner, 'dinner_songs.json')


def get_cache_featured_songs():
    if not os.path.isfile(ROOT_CACHE + '\\featured_playlist.json'):
        cache_featured_playlist()
        with open(ROOT_CACHE + '\\featured_playlist.json') as songs:
            temp = json.loads(songs.read())
            return {'songs': temp}
    if os.path.getsize(ROOT_CACHE + '\\featured_playlist.json') <= 0:
        cache_featured_playlist()
        with open(ROOT_CACHE + '\\featured_playlist.json') as songs:
            temp = json.loads(songs.read())
            return {'songs': temp}
    with open(ROOT_CACHE + '\\featured_playlist.json') as songs:
        temp = json.loads(songs.read())
        return {'songs': temp}


def get_cached_category_songs(category):
    if not os.path.isfile(ROOT_CACHE + '\\' + category + '_songs.json'):
        cache_category_songs()
        with open(ROOT_CACHE + '\\' + category + '_songs.json') as songs:
            temp = json.loads(songs.read())
            return {'songs': temp}
    if os.path.getsize(ROOT_CACHE + '\\' + category + '_songs.json') <= 0:
        cache_category_songs()
        with open(ROOT_CACHE + '\\' + category + '_songs.json') as songs:
            temp = json.loads(songs.read())
            return {'songs': temp}
    with open(ROOT_CACHE + '\\' + category + '_songs.json') as songs:
        temp = json.loads(songs.read())
        return {'songs': temp}
