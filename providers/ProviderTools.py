import json
from typing import Union

from providers import YandexMusicProvider, SpotifyProvider, TrackInfo
from settings import SETTINGS

YANDEX_PROVIDER: YandexMusicProvider = None
SPOTIFY_PROVIDER: SpotifyProvider = None

def init_providers():
    """
    Initialize providers `YANDEX_PROVIDER` and `SPOTIFY_PROVIDER` and parse tokens
    :return: credentials
    """
    global YANDEX_PROVIDER, SPOTIFY_PROVIDER
    if not YANDEX_PROVIDER and not SPOTIFY_PROVIDER:
        YANDEX_PROVIDER = YandexMusicProvider(SETTINGS.YANDEX_TOKEN)
        SPOTIFY_PROVIDER = SpotifyProvider(SETTINGS.SPOTIFY_CLIENT, SETTINGS.SPOTIFY_SECRET)

    return YANDEX_PROVIDER, SPOTIFY_PROVIDER

def convert_ya_to_spot(url: str, limit: int) -> list[TrackInfo]:
    """
    Convert yandex track URL to spotify one
    :param limit: tracks limit
    :param url: URL to the yandex track
    :return: tracks info
    """
    track = YANDEX_PROVIDER.get_track_by_url(url)
    query = f'{track.title} {track.albums[0]} {track.artists[0]}'
    return SPOTIFY_PROVIDER.search(query, limit)

def convert_spot_to_ya(url: str, limit: int) -> list[TrackInfo]:
    """
    Convert spotify track URL to yandex one
    :param url: track URL
    :param limit: tracks limit
    :return: tracks info
    """
    track = SPOTIFY_PROVIDER.get_track_by_url(url)
    query = f'{track.title} {track.albums[0]} {track.artists[0]}'
    return YANDEX_PROVIDER.search(query, limit)