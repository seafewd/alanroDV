import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# authenticate with the following first
#set SPOTIPY_CLIENT_ID=<clientId>
#set SPOTIPY_CLIENT_SECRET=<clientSecret>
#set SPOTIPY_CLIENT_URI=https://google.com/

# username NatBQIsXTr6SVGLut8wgYQ
username = "NatBQIsXTr6SVGLut8wgYQ"

# save query
# query = sys.argv[1]

# user id: seafood?si=NatBQIsXTr6SVGLut8wgYQ

# erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# spotify object
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
username = user['display_name']
while True:
    print()
    print("Spotipy search thingie - welcome, " + username)
    print()
    print("0 - Exit")
    print("1 - Search for a track")
    print("2 - Search for an artist")
    choice = input("Enter... ")

    if choice == "0":
        break
    if choice == "1":
        print()
        query = input("Enter track name: ")
        print()

        # get search results for track
        searchResults = spotifyObject.search(query, 5, type="track")
        #print(json.dumps(searchResults, indent = 4, sort_keys=True))
        searchResults = searchResults['tracks']['items']

        for track in searchResults:
            # track details
            songName = track['name']
            artist = track['album']['artists']['name']
            album = track['album']['name']
            releaseDate = track['album']['release_date']
            print("Track name:   " + songName)
            print("Artist:       " + artist)
            print("Album:        " + album)
            print("Release date: " + releaseDate)
            print("")
    if choice == "2":
        print()
        query = input("Enter artist name: ")
        print()

        # get search results for artist
        searchResults = spotifyObject.search(query, type="artist")
        # artist details
        artist = searchResults['artists']['items'][0]
        print("Artist: " + artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print("Genres: " + artist['genres'][0] + ", " + artist['genres'][1])
        #webbrowser.open(artist['images'][0]['url'])

        #print(displayName)
        #print(json.dumps(searchResults, indent = 4, sort_keys=True))
    print("-----------------------------------------------")
