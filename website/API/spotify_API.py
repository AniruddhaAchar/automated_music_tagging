from pprint import pprint
from Machine_Learning import classifier
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

user_name = "Aniruddha"
scope = 'user-library-read'
client_credentials_manager = SpotifyClientCredentials(client_id="3d7faefb8409449e8c8d8ca800bf2f5a",
                                                      client_secret='ac202cb275c7480aaf162ca99b98688c')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
featured_play_lists = sp.featured_playlists(country='US', limit=10).get('playlists').get('items')


def get_featured_songs():
    """
    This function extracts song's details from the featured play lists on Spotify.
     Song details contains information about the artist, title, album, images
    :return: a list of song details.
    """
    track_details = []
    for featured_playlist in featured_play_lists:
        play_list_details = sp.user_playlist_tracks(playlist_id=featured_playlist.get('id'),
                                                    user=featured_playlist.get('owner').get('id'), limit=4)
        for item in play_list_details.get('items'):
            artist_names = []
            album_name = item.get('track').get('album').get('name')
            images = item.get('track').get('album').get('images')  # a list if images with the height, width and the
            # url to the image
            for artist in item.get('track').get('album').get('artists'):
                artist_names.append(artist.get('name'))
            track_name = item.get('track').get('name')
            audio_features = sp.audio_features([item.get('track').get('uri')])[0]
            activity_class = classifier.classify_track(audio_features)
            # selecting only 64 x 64 url
            details = {'name': track_name, 'artists': artist_names, 'images': images[2], 'album': album_name, 'activity_class': activity_class}
            track_details.append(details)
    return track_details

# todo write api calls for getting details specific to activities.
# todo write functions to process and classify a given audio file.
# todo write function to search and the classify track from spotify.
