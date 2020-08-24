import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# authenticate with the following first
#export SPOTIPY_CLIENT_ID=your-spotfiy-client-id
#export SPOTIPY_CLIENT_SECRET=your-spotify-client-secret
#export SPOTIPY_CLIENT_URI=your-spotify-client-uri
#export SPOTIPY_REDIRECT_URI=your-spotify-redirect-uri

username = "your-spotify-user-name"

# save query
# query = sys.argv[1]

# erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    if os.path.exists(f".cache-{username}"):
      os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# spotify object
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
username = user['display_name']
resultLimit =  5

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
        searchResults = spotifyObject.search(query, resultLimit, type="track")
        #print(json.dumps(searchResults, indent = 4, sort_keys=True))
        searchResults = searchResults['tracks']['items']

        print("Displaying the top " + str(resultLimit) + " tracks.")
        print("")

        for track in searchResults:
            # track details
            songName = track['name']
            artist = track['album']['artists'][0]['name']
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
        searchResults = spotifyObject.search(query, resultLimit, type="artist")
        searchResults = searchResults['artists']['items']

        print("Displaying the top " + str(resultLimit) + " artists.")
        print("")

        for artist in searchResults:

            # artist details
            artistName = artist['name']
            followers = str(artist['followers']['total'])
            genres = artist['genres']

            print("Artist:    " + artistName)
            print("Followers: " + followers)
            print("Genres:    ", end="")
            for genre in genres:
                print(genre, end=", ")
            print("")
            print("")
            #webbrowser.open(artist['images'][0]['url'])

        #print(displayName)
        #print(json.dumps(searchResults, indent = 4, sort_keys=True))
    print("-----------------------------------------------")
