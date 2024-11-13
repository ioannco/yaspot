import json
from typing import Union

from providers import YandexMusicProvider, SpotifyProvider, TrackInfo

YANDEX_PROVIDER: YandexMusicProvider = None
SPOTIFY_PROVIDER: SpotifyProvider = None

def init_providers():
    """
    Initialize providers `YANDEX_PROVIDER` and `SPOTIFY_PROVIDER` and parse tokens
    :return: credentials
    """

    credentials = load_credentials()
    if not credentials:
        print('Credentials file not found. Read "Readme.txt" for more information.')
        exit(1)

    global YANDEX_PROVIDER, SPOTIFY_PROVIDER
    if not YANDEX_PROVIDER and not SPOTIFY_PROVIDER:
        YANDEX_PROVIDER = YandexMusicProvider(credentials["YANDEX_TOKEN"])
        SPOTIFY_PROVIDER = SpotifyProvider(credentials["SPOTIFY_CLIENT"], credentials["SPOTIFY_SECRET"])

    return credentials, YANDEX_PROVIDER, SPOTIFY_PROVIDER

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

def load_credentials() -> Union[dict[str, str], None]:
    """
    Load credentials from "credentials.json" file.
    :return: credentials dict if successful, None otherwise
    """
    try:
        with open('credentials.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print('Credentials file not found.')
        return None