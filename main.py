import spotipy
import json
import ytmusicapi
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth


def main():
    # spotify=authenticate_spotify()
    # playlists=get_playlists(spotify)
    # user_id=get_user_id(spotify)

    # tracks_list=get_tracks(spotify, '0UuAzJcX1PDq5BZtnnJgqg')

    # i = 1
    # for result in tracks_list:
    #     for track in result['items']:
    #         print(f'{i}. {track['item']['name']} by {track['item']['artists'][0]['name']}')
    #         i += 1
    # print(spotify.playlist_items('0UuAzJcX1PDq5BZtnnJgqg', limit=10, offset=0))
    youtube = authenticate_yt()
    # print(json.dumps(search_youtube(youtube, 'Girls'), indent=2))


def authenticate_spotify():
    config = dotenv_values(r"D:\code\py\Youtify\client.env")
    scope = "playlist-read-private"
    auth_spotify = spotipy.Spotify(
        auth_manager=(
            SpotifyOAuth(
                client_id=config["SPOTIPY_CLIENT_ID"],
                client_secret=config["SPOTIPY_CLIENT_SECRET"],
                redirect_uri=config["SPOTIPY_REDIRECT_URL"],
                scope=scope,
            )
        )
    )
    return auth_spotify


def get_playlists(authenticated_spotify):
    playlists = authenticated_spotify.current_user_playlists()
    return playlists


def get_user_id(authenticated_spotify):
    user_id = authenticated_spotify.current_user()["id"]
    return user_id


def get_tracks(authenticated_spotify, playlist_id):
    # tracks=[]
    # offset=0
    # while True:
    #     json_page=authenticated_spotify.playlist_items(playlist_id, limit=100, offset=offset)
    #     for result in json_page:

    #     if result['next']==None or result['next']=='null':
    #         break
    #     offset += 100
    # return tracks
    ...


def authenticate_yt():
    youtube = ytmusicapi.YTMusic("browser.json")
    return youtube


def search_youtube(authenticated_yt, track):
    results = authenticated_yt.search(track)
    return results


if __name__ == "__main__":
    main()
