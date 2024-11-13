import json
import trace
from typing import Union

from providers import YandexMusicProvider, MusicProviderAPI, SpotifyProvider


def main():
    credentials = load_credentials()
    if not credentials:
        print('Credentials file not found. Read "Readme.txt" for more information.')
        exit(1)

    ya = YandexMusicProvider(credentials["YANDEX_TOKEN"])
    sp = SpotifyProvider(credentials["SPOTIFY_CLIENT"], credentials["SPOTIFY_SECRET"])

    while True:
        url = input("Please, provide yandex music track URL:\n")

        if not url:
            exit(0)

        try:
            track = ya.get_track_by_url(url)
            query = f'{track.title} {track.albums[0]} {tr}'

            res = sp.search(query, limit = 1)

            if not res:
                print('Spotify track not found')
                continue

            print(res[0].url)

        except MusicProviderAPI.TrackNotFoundException:
            print('Track not found.')


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


if __name__ == '__main__':
    main()
    exit(0)
