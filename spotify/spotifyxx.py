import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#get username
username = sys.argv[1]

#user id: seafood?si=NatBQIsXTr6SVGLut8wgYQ

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

#create spotifyObject
spotifyObject = spotipy.Spotify(auth=token)
