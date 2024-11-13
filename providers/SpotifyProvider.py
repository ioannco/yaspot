from spotipy import SpotifyOAuth, SpotifyClientCredentials, Spotify

from providers import MusicProviderAPI, TrackInfo


class SpotifyProvider(MusicProviderAPI):
    def __init__(self, client_id: str, secret: str):
        super().__init__()
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret)
        self.client = Spotify(auth_manager=auth_manager)

    def get_track_by_url(self, url: str) -> TrackInfo:
        raise RuntimeError("Not implemented")

    def get_track_by_id(self, id: str) -> TrackInfo:
        raise RuntimeError("Not implemented")

    def search(self, query: str, limit: int = 10) -> list[TrackInfo]:
        res = self.client.search(query, limit=limit, type='track', market='NL')
        return  [TrackInfo(
            "Spotify",
            track['id'],
            track['name'],
            [artist['name'] for artist in track['artists']],
            [track['album']['name']],
            track['external_urls']['spotify'],
            track
        ) for track in res['tracks']['items']]





