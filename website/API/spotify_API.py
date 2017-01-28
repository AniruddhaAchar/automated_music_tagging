import json

from Machine_Learning import classifier
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

user_name = "Aniruddha"
scope = 'user-library-read'
client_credentials_manager = SpotifyClientCredentials(client_id="3d7faefb8409449e8c8d8ca800bf2f5a",
                                                      client_secret='ac202cb275c7480aaf162ca99b98688c')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

track_details = []


def get_featured_songs():
    """
    This function extracts song's details from the featured play lists on Spotify.
     Song details contains information about the artist, title, album, images
    :return: a list of song details.
    """
    featured_play_lists = sp.featured_playlists(country='US', limit=10).get('playlists').get('items')
    for featured_playlist in featured_play_lists:
        play_list_details = sp.user_playlist_tracks(playlist_id=featured_playlist.get('id'),
                                                    user=featured_playlist.get('owner').get('id'), limit=4)
        for item in play_list_details.get('items'):
            artist_names = []
            album_name = item.get('track').get('album').get('name')
            images = item.get('track').get('album').get(
                'images')  # a list if images with the height, width and the url to the image
            for artist in item.get('track').get('album').get('artists'):
                artist_names.append(artist.get('name'))
            track_name = item.get('track').get('name')
            audio_features = sp.audio_features([item.get('track').get('uri')])[0]
            print(track_name, item.get('track').get('uri'))
            activity_class = classifier.classify_track(audio_features)
            details = {'name': track_name, 'artists': artist_names, 'images': images, 'album': album_name,
                       'activity_class': activity_class}
            if details['activity_class'] == 0:
                continue
            track_details.append(details)

    return json.dumps(track_details)


def search_song(title):
    search_result = sp.search(title, limit=2)
    items = search_result.get('tracks').get('items')
    track_details = []
    for item in items:
        artist_names = []
        images = item.get('album').get('images')  # a list if images with the height, width and the
        for artist in item.get('album').get('artists'):
            artist_names.append(artist.get('name'))
        track_name = item.get('name')
        audio_features = sp.audio_features([item.get('uri')])[0]
        activity_class = classifier.classify_track(audio_features)
        details = {'name': track_name, 'artists': artist_names, 'images': images, 'activity_class': activity_class}
        track_details.append(details)
    return track_details


def get_category_songs(category):
    category = category.lower()
    dinner_seed_track = ['7jib7AfCM6wU5KjaA6Zt5d', '1ykNjOQbYJgZE3pflVB9MN', '00CIFNT8kOm61dupysBFp8',
                         '6CDQBADsdzJwc3qZ3OPDHH', '4dn6rw5Ze1uWrLm1uOk1gu']
    party_seed_track = ['4Ce37cRWvM1vIGGynKcs22', '1mSlftOO1dlDRXAyOE0Sbd', '7BKLCZ1jbUBVqRi2FVlTVw',
                        '1vvNmPOiUuyCbgWmtc6yfm', '3XIIOCu6B8PuGq5j61asEM']
    sleep_seed_track = ['645kj2wJDlXW7Wnx5N9WCq', '3aLof1zmaQ0GLcAc9YQ3Fq', '1gVXTJVSekOTCH8hhibcqi',
                        '07Hk13m0dIGWhGr9B4yEsJ', '2vr6fjMZm1pliQ3a6HL8MT']
    workout_seed_track = ['6or1bKJiZ06IlK0vFvY75k', '5YEOzOojehCqxGQCcQiyR4', '6JyuJFedEvPmdWQW0PkbGJ',
                          '2Vo3sVSCltAaYU1u0f9ASz', '3U8Ev1gISsx6O1uwpsttOD']
    recommendations = None
    track_details = []
    if category == 'dinner':
        recommendations = sp.recommendations(seed_tracks=dinner_seed_track, limit=10, country='US').get('tracks')
    elif category == 'party':
        recommendations = sp.recommendations(seed_tracks=party_seed_track, limit=10, country='US').get('tracks')
    elif category == 'sleep':
        recommendations = sp.recommendations(seed_tracks=sleep_seed_track, limit=10, country='US').get('tracks')
    elif category == 'workout':
        recommendations = sp.recommendations(seed_tracks=workout_seed_track, limit=10, country='US').get('tracks')

    for recommendation in recommendations:
        images = recommendation.get('album').get('images')
        artist_names = []
        for artist in recommendation.get('artists'):
            artist_names.append(artist.get('name'))
        track_name = recommendation.get('name')
        album_name = recommendation.get('album').get('name')
        audio_features = sp.audio_features(recommendation.get('uri'))[0]
        activity_class = classifier.classify_track(audio_features)
        details = {'name': track_name, 'artists': artist_names, 'images': images, 'activity_class': activity_class}
        track_details.append(details)
    return json.dumps(track_details)
