import spotipy
import json
import re
from rapidfuzz import fuzz
import ytmusicapi
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth
import csv


def main():
    # spotify=authenticate_spotify()
    # playlists=get_playlists(spotify)
    # user_id=get_user_id(spotify)
    # # tracks_list=get_tracks(spotify, '0UuAzJcX1PDq5BZtnnJgqg')
    # tracks_list=get_tracks(spotify, '0GLFBA6h4AfwOPCbcWQwKN')
    # save_tracks(tracks_list, 'Tere Liye (Lofi Mix)')

    # print(json.dumps(tracks_list, indent=2))

    # for playlist in playlists['items']:
    #     if playlist['owner']['id'] == user_id:
    #         print(json.dumps(playlist, indent=2))

    youtube = authenticate_yt()
    results = clean_yt_results(search_yt(youtube, "Shape of You"))
    # print(json.dumps(results, indent=2))
    # print(json.dumps(search_yt(youtube, "Shape of You"), indent=2))

    list = []
    with open("spotify.csv", "r") as file:
        reader = csv.DictReader(file)
        i = 1
        for row in reader:
            print(f"{i}. {row['track_name']} by {row['artist_name']}.")
            list.append(row)
            i += 1

    choice = int(input("Which track to search? : "))
    spotify_track = {
        "track_name": list[choice - 1]["track_name"],
        "artist_name": list[choice - 1]["artist_name"],
        "duration": int(list[choice - 1]["duration(s)"]),
    }
    yt_list = clean_yt_results(search_yt(youtube, spotify_track["track_name"]))
    # yt_list = (search_yt(youtube, "Shape of You"))
    yt_list = score(spotify_track, yt_list)
    
    # yt_list=(search_yt(youtube, spotify_track["track_name"]))
    print(json.dumps(yt_list, indent=2))

    ...


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


def save_spotify_tracks(tracks_list: list, track_name: str):
    for track in tracks_list[0]:
        # print(track[0]['item'])
        if track["item"]["name"] == track_name:
            # print(json.dumps(track, indent=2))
            # print(f'{track['item']['name']} and {track['item']['artists'][0]['name']}')
            with open("spotify.csv", "a", newline="") as file:
                writer = csv.DictWriter(
                    file, fieldnames=["track_name", "artist_name", "duration(s)"]
                )
                writer.writerow(
                    {
                        "track_name": track["item"]["name"],
                        "artist_name": track["item"]["artists"][0]["name"],
                        "duration(s)": round(int(track["item"]["duration_ms"]) / 1000),
                    }
                )


def _get_tracks(authenticated_spotify, playlist_id) -> list:
    tracks = []
    offset = 0

    json_page = authenticated_spotify.playlist_items(
        playlist_id, limit=10, offset=offset
    )
    tracks.append(json_page.get("items", []))

    return tracks


def authenticate_yt() -> ytmusicapi.YTMusic:
    youtube = ytmusicapi.YTMusic("browser.json")
    return youtube


def create_playlist(authenticated_yt):
    authenticated_yt.create_playlist(
        "zzz__TestPLaylist__delete_later", "Test playlist, delete later."
    )


def search_yt(authenticated_yt, track) -> list:
    results = authenticated_yt.search(track, filter="songs")
    return results


def save_youtube_tracks(): ...


def clean_yt_results(json_page: list) -> list[dict]:
    filtered_list = []
    for result in json_page:
        filtered_list.append(
            {
                "track_name": result["title"],
                "artist_name": result["artists"][0],
                "duration": result["duration_seconds"],
                "id": result["videoId"],
                "views": result["views"],
            }
        )
    return filtered_list


def clear_track_name(name: str) -> str:
    name = name.strip()
    # if version==False:
    #     junk_pattern = r"\(.*?\)|\[.*?\]"
    #     name = re.sub(junk_pattern, "", name)
    junk_words = ["official", "video", "audio", "lyric", "lyrics", "hd", "4k", "mv"]
    for junk_word in junk_words:
        name = name.replace(junk_word, "")
    return name


def extract_keywords(track_name: str) -> set[str]:
    KEYWORDS = [
    "remix", "instrumental", "acapella", "reverb", "slowed", "sped up",
    "nightcore", "extended", "radio edit", "live", "acoustic", "cover",
    "remaster", "remastered", "clean", "band", "bonus track",
    "demo", "edit", "mix", "version", r"lo-?fi",  r"radio\s+edit", r"sped\s+up"
]
    name = track_name.lower()
    found = set()
    for keyword in KEYWORDS:
        pattern = r'\b' + re.escape(keyword).replace(r'\ ', r'\s+') + r'\b'
        if re.search(pattern, name):
            found.add(keyword)
    return found


def is_keyword_mismatch(track_a: str, track_b: str) -> bool:
    keyword_a = extract_keywords(track_a)
    keyword_b = extract_keywords(track_b)
    if not keyword_a and not keyword_b:
        return False
    return keyword_a.isdisjoint(keyword_b)


def score(source_track: dict, target_track: list):
    scored_tracks = []
    scored_track = {}
    for track in target_track:
        if is_keyword_mismatch(source_track["track_name"], track["track_name"]):
            continue
        track["track_name"] = ((track["track_name"]).lower())
        _source_name = (source_track["track_name"].lower())

        title_score: int = round(
            fuzz.token_sort_ratio(_source_name, track["track_name"])
        )
        artist_score: int = round(
            fuzz.token_sort_ratio(
                (source_track["artist_name"]).lower(),
                (track["artist_name"]["name"]).lower(),
            )
        )

        if track["duration"] == None:
            total_score = title_score * 0.51 + artist_score * 0.49
        else:
            difference = abs(source_track["duration"] - track["duration"])
            if 0 <= difference <= 5:
                duration_score: int = 100 - 20 * difference
            else:
                duration_score: int = 0
            total_score = (
                title_score * 0.5 + artist_score * 0.35 + duration_score * 0.15
            )
        scored_track = track
        scored_track["score"] = total_score
        scored_tracks.append(scored_track)
    return scored_tracks


if __name__ == "__main__":
    main()
