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

    youtube = authenticate_yt()
    yt_results=search_youtube(youtube, 'Girls')
    print(json.dumps(yt_results, indent=2))


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


def create_playlist(authenticated_yt):
    authenticated_yt.create_playlist('zzz__TestPLaylist__delete_later', 'Test playlist, delete later.')


def search_youtube(authenticated_yt, track):
    results = authenticated_yt.search(track)
    return results


if __name__ == "__main__":
    main()