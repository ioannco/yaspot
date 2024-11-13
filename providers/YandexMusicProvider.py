import re

from . import MusicProviderAPI, TrackInfo
from yandex_music import Client, Track


def _yandex_track_to_track_info(track: Track) -> TrackInfo:
    return TrackInfo(
        "YandexMusic",
        track.track_id,
        track.title,
        [artist.name for artist in track.artists],
        [album.title for album in track.albums],
        f'https://music.yanndex.ru/album/{track.albums[0].id}/track/{track.id}',
        track.albums[0].year,
        track.cover_uri.replace('%%', '200x200'),
        track)


class YandexMusicProvider(MusicProviderAPI):
    ID_FROM_URL_REGEX = re.compile(r".*music\.yandex\.ru/album/(\d*)/track/(\d*).*")

    def __init__(self, token):
        super().__init__()
        self.client = Client(token).init()

    def get_track_by_url(self, url: str) -> TrackInfo:
        """
        Get track
        :param url: url to yandex music
        :return: track
        """
        info_from_url = self.ID_FROM_URL_REGEX.match(url).groups()
        if not info_from_url or len(info_from_url) != 2:
            raise MusicProviderAPI.TrackNotFoundException("Unable to parse url.")

        track_id = int(info_from_url[1])
        album_id = int(info_from_url[0])

        return self.get_track_by_id(f'{track_id}:{album_id}')

    def get_track_by_id(self, id: str):
        """
        Get yandex track by id
        :param id: id
        :return: track
        """
        tracks = self.client.tracks([id])
        if not tracks:
            raise MusicProviderAPI.TrackNotFoundException("Unable find track.")

        track = tracks[0]
        return _yandex_track_to_track_info(track)

    def search(self, query: str, limit: int = 10) -> list[TrackInfo]:
        """
        Search for tracks
        :param query: search query
        :param limit: list limit
        :return: list of tracks
        """
        res = self.client.search(query, type_='track')
        if res.tracks:
            return [_yandex_track_to_track_info(track) for track in res.tracks.results]
        return []

