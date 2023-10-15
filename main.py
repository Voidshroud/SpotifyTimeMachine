import os
import requests
import bs4
import spotipy
from spotipy.oauth2 import SpotifyOAuth

while True:
    dateInput = input("Which year do you want to travel to? (DD/MM/YYYY): ")

    if int(dateInput.split("/")[2]) >= 1958:
        dateList = dateInput.split("/")
        dateList.reverse()
        destinationDate = "-".join(dateList)
        print(f"Traveling to {dateInput}")
        break
    else:
        print("Please choose date after 04/08/1958")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{destinationDate}/")

soup = bs4.BeautifulSoup(response.text, "html.parser")

songs = []

firstSongData = soup.find(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")
songs.append(firstSongData.get_text().strip("\n\t"))

songsData = soup.find_all(name="h3", id="title-of-a-story", class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
for song in songsData:
    songs.append(song.get_text().strip("\n\t"))

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("ID"),
                                               client_secret=os.environ.get("SECRET"),
                                               redirect_uri="https://open.spotify.com/",
                                               scope="playlist-modify-private"))

userID = sp.me()["id"]
playlist = sp.user_playlist_create(userID, f"Top 100 - {dateInput}", False, False, f"Top 100 chart for {dateInput}")


for song in songs:
    try:
        result = sp.search(song)
        songToAdd = [result['tracks']['items'][0]['external_urls']['spotify'].split('/')[-1]]
        sp.playlist_add_items(playlist["id"], songToAdd)
        print(f"'{song}' has been added to the playlist 'Top 100 - {dateInput}'.")

    except:
        print(f"{song} not found.")
