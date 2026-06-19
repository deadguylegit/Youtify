from dotenv import dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

config = dotenv_values(r"D:\code\py\Youtify\client.env")

scope = "playlist-read-private"
spotify = spotipy.Spotify(
    auth_manager=(
        SpotifyOAuth(
            client_id=config["SPOTIPY_CLIENT_ID"],
            client_secret=config["SPOTIPY_CLIENT_SECRET"],
            redirect_uri=config["SPOTIPY_REDIRECT_URL"],
            scope=scope,
        )
    )
)
user_id=spotify.current_user()['id']
results = spotify.current_user_playlists()

for result in results['items']:
    if result['owner']['id']==user_id:
        print(json.dumps(result, indent=1))

