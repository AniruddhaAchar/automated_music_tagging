import spotipy
import spotipy.util as util
import time
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint
from Database_connections import addTrack


def getTrackDetails(tracks):
    tracks = tracksjson.get("items")
    for track in tracks:
        details = track.get("track")
        #pprint(details)
        if details.get(u"artists") and details.get("name"):
            print ("Track name: {}, Track artist: {}, Track URI: {}, id: {}, preview {}".format(details.get("name").encode("utf8"),
                                                                       details.get(u"artists"),
                                                                      details.get(u"uri").encode("utf8"), details.get(u"id"),details.get("preview_url")))
            artists = ""
            for artist in details.get("artists"):
                artists += artist.get("name")+", "
            track_uri = [details.get(u"uri")]
            id = details.get(u"id")
            uri = details.get(u"uri")
            name = details.get("name")
            audio_features = sp.audio_features(track_uri)
            features = audio_features[0]
            acousticness =features['acousticness']
            danceability = features['danceability']
            duration_ms = features['duration_ms']
            energy =features['energy']
            instrumentalness = features['instrumentalness']
            key = features['key']
            liveness = features['liveness']
            loudness = features['loudness']
            mode = features['mode']
            speechiness = features['speechiness']
            tempo = features['tempo']
            time_signature =features['time_signature']
            valence =features['valence']
            time.sleep(1)
            #if id not in added_list:
                #added_list.append(id)
                #addTrack(id=id, name = name, uri=uri, artist=artists, acousticness=acousticness, danceability=danceability, duration_ms=duration_ms, energy=energy,instrumentalness=instrumentalness, key=key, liveness=liveness, mode=mode, speechiness=speechiness, tempo=tempo, time_signature=time_signature, valence=valence, loudness=loudness)

user_name = "Aniruddha"
scope = 'user-library-read'
redirect = "http://localhost:8080/callback"
client_credentials_manager = SpotifyClientCredentials(client_id='3d7faefb8409449e8c8d8ca800bf2f5a',client_secret='ac202cb275c7480aaf162ca99b98688c')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False
added_list = []
token = util.prompt_for_user_token(username=user_name, client_secret='ac202cb275c7480aaf162ca99b98688c',
                                   client_id='3d7faefb8409449e8c8d8ca800bf2f5a',
                                   redirect_uri="http://localhost:8080/callback")
tracks = ["spotify:track:7BKLCZ1jbUBVqRi2FVlTVw"]
#pprint (sp.audio_features(tracks))
if token:
    catagory_playlist = sp.category_playlists(category_id="sleep", country="US")
    for playlist in catagory_playlist.get("playlists").get("items"):
        print ("Name: {}, playlist_id = {}, user ={}".format(playlist.get("name"), playlist.get("id"),
                                                            playlist.get(u'owner').get("id")))
        playlist_id = playlist.get("id")
        user = playlist.get(u'owner').get("id")
        tracksjson = sp.user_playlist_tracks(playlist_id=playlist_id, user=user)
        getTrackDetails(tracksjson)
        print ("\n" * 4)

else:
    print ("Token failed")
