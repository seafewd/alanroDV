import spotipy.oauth2 as oauth2
client_id = "47fd89a9ede440dcb0c0c54c76afd6a3"
client_secret = "c2a497b9d5114e19b14650b74364b9cf"

credentials = oauth2.SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret)


token = credentials.get_access_token()

# Create new API object wrapper
spotify = spotipy.Spotify(auth=token)
