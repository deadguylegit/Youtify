import spotipy
import json
import re
from thefuzz import fuzz
import ytmusicapi
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth


def main():
    # spotify=authenticate_spotify()
    # playlists=get_playlists(spotify)
    # user_id=get_user_id(spotify)
    # tracks_list=get_tracks(spotify, '0UuAzJcX1PDq5BZtnnJgqg')
    # print(json.dumps(tracks_list, indent=2))

    youtube = authenticate_yt()
    yt_results = search_youtube(youtube, "Junoon")
    list = []
    for result in yt_results:
        list.append(
            {
                "track_name": result["title"],
                "artist_name": result["artists"][0],
                "duration (s)": result["duration_seconds"],
            }
        )
    # print(json.dumps(yt_results, indent=2))
    print(json.dumps(list, indent=2))


def authenticate_spotify() -> spotipy.Spotify:
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


def get_playlists(authenticated_spotify) -> dict:
    playlists = authenticated_spotify.current_user_playlists()
    return playlists


def get_user_id(authenticated_spotify) -> str:
    user_id = authenticated_spotify.current_user()["id"]
    return user_id


def get_tracks(authenticated_spotify, playlist_id) -> list:
    tracks = []
    offset = 0
    while True:
        json_page = authenticated_spotify.playlist_items(
            playlist_id, limit=100, offset=offset
        )
        tracks.append(json_page.get("items", []))
        if json_page["next"] == None or json_page["next"] == "null":
            break
        offset += 100

    return tracks


def authenticate_yt() -> ytmusicapi.YTMusic:
    youtube = ytmusicapi.YTMusic("browser.json")
    return youtube


def create_playlist(authenticated_yt):
    authenticated_yt.create_playlist(
        "zzz__TestPLaylist__delete_later", "Test playlist, delete later."
    )


def search_youtube(authenticated_yt, track) -> list:
    results = authenticated_yt.search(track, filter="songs")
    return results


def clear_track_name(name: str) -> str:

    name.strip()
    tags = r"\(.*?remix.*?\)|\(.*?lo-?fi.*?\)|\(.*?acoustic.*?\)|\(.*?radio\s+edit.*?\)|\(.*?version.*?\)|\(.*?live.*?\)|\(.*?remaster.*?\)|\(.*?extended.*?\)|\(.*?sped\s+up.*?\)|\(.*?slowed.*?\)|\(.*?reverb.*?\)"
    if re.search(tags, name):
        junk_pattern = r"\(.*?\)|\[.*?\]"
        name = re.sub(junk_pattern, "", name)
    junk_words = ["official", "video", "audio", "lyric", "lyrics", "hd", "4k", "mv"]
    for junk_word in junk_words:
        name.replace(junk_word, "")
    return name


def score(source_track: dict, target_track: list):
    source_name, source_artist, source_duration = (
        source_track["track_name"],
        source_track["artist_name"],
        source_track["duration"],
    )
    # source_name, source_artist, source_duration = source_track['track_name'], source_track['artist_name'], source_track['duration']
    for track in target_track:
        title_score: int = fuzz.token_sort_ratio(source_name, track["track_name"])
        artist_score: int = fuzz.token_sort_ratio(source_artist, track["artist_name"])
        duration_score: int = fuzz.token_sort_ratio(source_duration, track["duration"])
        yield (source_track, (title_score * 0.35 + artist_score * 0.5 + duration_score * 0.15), track)


if __name__ == "__main__":
    main()
