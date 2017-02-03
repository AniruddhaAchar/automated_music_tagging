from flask_restful import Resource, reqparse, abort

from API.spotify_API import search_song
from cache_data import get_cache_featured_songs, get_cached_category_songs


class FeaturedPlaylist(Resource):
    def get(self):
        return get_cache_featured_songs()


class CategorySongs(Resource):
    def get(self, category):
        if category not in ['party', 'dinner', 'sleep', 'workout']:
            abort(404, message="No such category")
        return get_cached_category_songs(category=category)


class SearchSongs(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('track', type=str, help='track cannot be converted')
        args = parser.parse_args()
        if args['track']:
            return search_song(args['track'])
        else:
            abort(404, message="Wrong parameters passed")
