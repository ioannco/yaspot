from typing import Any

class TrackInfo:
    """
    Basic track information response
    """
    def __init__(self, provider: str, id: str, title: str, artists: list[str], albums: list[str], url: str, year: int, thumbnail: str, provider_container: Any):
        self.provider = provider
        self.id = id
        self.title = title
        self.artists = artists
        self.albums = albums
        self.url = url
        self.year = year
        self.thumbnail = thumbnail
        self.provider_container = provider_container

    def __str__(self):
        return self.__dict__.__str__()

    provider: str
    id: str
    title: str
    artists: list[str]
    albums: list[str]
    url: str
    year: int
    thumbnail: str
    provider_container: Any

class MusicProviderAPI:
    class TrackNotFoundException(Exception):
        def __init__(self, msg):
            super().__init__(msg)

    client = None

    def __init__(self):
        pass

    def get_track_by_url(self, url: str) -> TrackInfo:
        """
        Get track info by url
        :param url: track url
        :return: info
        """
        pass


    def get_track_by_id(self, id: str) -> TrackInfo:
        """
        Get track info by id
        :param id: track provider id
        :return: info
        """
        pass


    def search(self, query: str, limit: int = 10) -> list[TrackInfo]:
        """
        Search tracks by query
        :param query: search query
        :param limit: response list len limit
        :return: list of track info
        """
        pass


