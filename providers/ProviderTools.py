import json
from typing import Union

from providers import YandexMusicProvider, SpotifyProvider


YANDEX_PROVIDER: YandexMusicProvider = None
SPOTIFY_PROVIDER: SpotifyProvider = None


def init_providers():
    """
    Initialize providers `YANDDEX_PROVIDER` and `SPOTIFY_PROVIDER` and parse tokens
    :return: credentials
    """
    credentials = load_credentials()
    if not credentials:
        print('Credentials file not found. Read "Readme.txt" for more information.')
        exit(1)

    global YANDEX_PROVIDER, SPOTIFY_PROVIDER
    YANDEX_PROVIDER = YandexMusicProvider(credentials["YANDEX_TOKEN"])
    SPOTIFY_PROVIDER = SpotifyProvider(credentials["SPOTIFY_CLIENT"], credentials["SPOTIFY_SECRET"])

    return credentials

def convert_ya_to_spot(url: str) -> str:
    """
    Convert yandex track URL to spotify one
    :param url: URL to the yandex track
    :return: URL to the spotify track
    """
    track = YANDEX_PROVIDER.get_track_by_url(url)
    query = f'{track.title} {track.albums[0]} {track.artists[0]}'

    res = SPOTIFY_PROVIDER.search(query, limit=1)
    if len(res) == 1:
        return res[0].url
    return ""


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