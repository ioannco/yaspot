import re

from . import MusicProviderAPI, TrackInfo
from yandex_music import Client

class YandexMusicProvider(MusicProviderAPI):
    ID_FROM_URL_REGEX = re.compile(r".*music\.yandex\.ru/album/(\d*)/track/(\d*).*")

    def __init__(self, token):
        super().__init__()
        self.client = Client(token).init()

    def get_track_by_url(self, url: str) -> TrackInfo:
        info_from_url = self.ID_FROM_URL_REGEX.match(url).groups()
        if not info_from_url or len(info_from_url) != 2:
            raise MusicProviderAPI.TrackNotFoundException("Unable to parse url.")

        track_id = int(info_from_url[1])
        album_id = int(info_from_url[0])

        return self.get_track_by_id(f'{track_id}:{album_id}')

    def get_track_by_id(self, id: str):
        tracks = self.client.tracks([id])
        if not tracks:
            raise MusicProviderAPI.TrackNotFoundException("Unable find track.")

        track = tracks[0]

        return TrackInfo(
            "YandexMusic",
            id,
            track.title,
            [artist.name for artist in track.artists],
            [album.title for album in track.albums],
            f'https://music.yanndex.ru/album/{id.split(":")[1]}/track/{id.split(":")[0]}',
            track
        )

