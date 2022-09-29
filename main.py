from pprint import pprint

import spotipy.oauth2
from bs4 import BeautifulSoup
import requests
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import DateTime

url = "https://www.billboard.com/charts/hot-100/"
client_id = ""
client_secret = ""
redirect_uri = ""
scope = ""

input_travel_year = input("What year would you like to travel to? Enter date format as YYYY-MM-DD: ")

response = requests.get(url=f"{url}{input_travel_year}/")
wepage_html = response.text

soup = BeautifulSoup(wepage_html, "html.parser")

songs = soup.select(selector="li #title-of-a-story")

song_names = [song.get_text().strip() for song in songs]

spotipy_response = spotipy.oauth2.SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                                               redirect_uri=redirect_uri)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope,
                              redirect_uri=redirect_uri,
                              client_id=client_id,
                              client_secret=client_secret,
                              show_dialog=True,
                              cache_path="token.txt"
                              )
)
user_id = sp.current_user()["id"]
song_uris = []
year = input_travel_year.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
        print(f"Song URI Added For Song: {song} URI: {uri}")
    except IndexError:
        print(f"No song uri found for song name: {song}")
    except AttributeError:
        print(f"No song uri found for song name: {song}")

playlist = sp.user_playlist_create(user=user_id, name=f"{input_travel_year} Billboard 100", public=False,
                                   description="This playlists consists of the top 100 songs from Empire Billboards Top 100 songs.")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)