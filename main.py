from dotenv import dotenv_values
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

config=dotenv_values(r'D:\code\py\Youtify\client.env')

scope='playlist-read-private'
sp=spotipy.Spotify(auth_manager=(SpotifyOAuth(client_id=config['SPOTIPY_CLIENT_ID'], client_secret=config['SPOTIPY_CLIENT_SECRET'], redirect_uri=config['SPOTIPY_REDIRECT_URL'], scope=scope)))
results=sp.current_user_playlists()
print(results)
