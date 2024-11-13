# Yandex Music to Spotify link converter telegram bot

This is an inline telegram bot with search and url convert capabilities

![preview](img.png)

## Installation
Before installation, you need to acquire Yandex Music token and Spotify 
client and secret tokens. You can find information about how to get them here: 
[Yandex API docs](https://yandex-music.readthedocs.io/en/main/token.html),
[Spotify API docs](https://developer.spotify.com/documentation/web-api/tutorials/getting-started)

To set up the bot running, you must also get bot token from [@botfather](t.me/botfather).
After your bot is ready, turn on inline mod by sending `/setinline` command to @botfather and 
setting prompt.

After you've got the tokens and the bot running, you'll need to fill this information into the `credentials.json`:
```json
{
  "YANDEX_TOKEN": "<Your yandex api token>",
  "SPOTIFY_CLIENT": "<Your spotify client token>",
  "SPOTIFY_SECRET": "<Your spotify secret token>",
  "TELEGRAM_TOKEN": "<Your telegram token from @botfather>"
}
```

Then you need to install pip requirements and activate python environment:

```shell
python -m venv .env
source .env/bin/activate #for UNIX (run activate.ps2 for windows)
pip install -r requirements.txt
```

# Usage
`python inline-bot.py`

