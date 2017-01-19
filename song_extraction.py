import urllib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import Database_connections

user_name = "Aniruddha"
scope = 'user-library-read'
redirect = "http://localhost:8080/callback"
client_credentials_manager = SpotifyClientCredentials(client_id='3d7faefb8409449e8c8d8ca800bf2f5a',client_secret='ac202cb275c7480aaf162ca99b98688c')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace = False

baseURL = "E:\\final year project\\audio files\\workout\\"

if True:
    sleepTrackIds = Database_connections.getTracksById(4, "workout",start=47)
    for sleepTrackId in sleepTrackIds:
        trackData = sp.track(sleepTrackId)
        preview_url = trackData.get("preview_url")
        if preview_url:
            name = str(trackData.get("name"))
            name = name.split("\"")
            name = name[0].split("\/")
            print(name[0])
            urllib.request.urlretrieve(preview_url,baseURL+name[0]+".mp3")
else:
    print("Auth failed")