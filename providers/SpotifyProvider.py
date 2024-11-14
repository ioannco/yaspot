import re

from spotipy import SpotifyClientCredentials, Spotify

from providers import MusicProviderAPI, TrackInfo
from settings import SETTINGS


def _spotify_track_to_track_info(track: dict):
    return TrackInfo(
            "Spotify",
            track['id'],
            track['name'],
            [artist['name'] for artist in track['artists']],
            [track['album']['name']],
            track['external_urls']['spotify'],
            int(track['album']['release_date'][:4]),
            track['album']['images'][2]['url'],
            track
    )


class SpotifyProvider(MusicProviderAPI):
    """
    Wrapper for spotify music api
    """
    SPOTIFY_ID_REGEX = re.compile(r'.*spotify\.com/track/(.*)')

    def __init__(self, client_id: str, secret: str):
        super().__init__()
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
        self.client = Spotify(auth_manager=auth_manager)

    def get_track_by_url(self, url: str) -> TrackInfo:
        """
        Get track info from spotify url
        :param url: link
        :return: track info
        """
        return self.get_track_by_id(self.SPOTIFY_ID_REGEX.match(url).group(0))

    def get_track_by_id(self, id: str) -> TrackInfo:
        """
        Get track info from spotify id
        :param id: track identifier
        :return: info
        """
        return _spotify_track_to_track_info(self.client.track(id, SETTINGS.SPOTIFY_MARKET_LOCALE))

    def search(self, query: str, limit: int = 10) -> list[TrackInfo]:
        """
        Search for track in Spotify
        :param query: search query. Can be enhanced with tags like :author :album etc.
        See official spotify api for more info.
        :param limit: result list size limit
        :return: info list
        """
        res = self.client.search(query, limit=limit, type='track', market=SETTINGS.SPOTIFY_MARKET_LOCALE)
        return  [_spotify_track_to_track_info(track) for track in res['tracks']['items']]





