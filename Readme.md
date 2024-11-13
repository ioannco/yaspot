# Yandex Music to Spotify link converter

This is a bacis tool for converting Yandex Music urls into Spotify urls

## Installation
Before installation, you need to acquire Yandex Music token and Spotify 
client and secret tokens. You can find information about how to get them here: 
[Yandex API docs](https://yandex-music.readthedocs.io/en/main/token.html),
[Spotify API docs](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

After you've got the tokens, you'll need to fill this information into the `credentials.json`:
```json
{
  "YANDEX_TOKEN": "<Your yandex api token>",
  "SPOTIFY_CLIENT": "<Your spotify client token>",
  "SPOTIFY_SECRET": "<Your spotify secret token>"
}
```

Then you need to install pip requirements and activate python environment:

```shell
python -m venv .env
source .env/bin/activate #for UNIX (run activate.ps2 for windows)
pip install -r requirements.txt
```

# Usage
`python main.py`

