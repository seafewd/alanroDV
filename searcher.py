import spotipy.oauth2 as oauth2
client_id = ""
client_secret = ""

credentials = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)


token = credentials.get_access_token()

# Create new API object wrapper
spotify = spotipy.Spotify(auth=token)
