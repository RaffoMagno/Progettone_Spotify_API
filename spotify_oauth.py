import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "b1ed2d5909a24d66912adc6f42531fee"
SPOTIFY_CLIENT_SECRET = "db711b1f9ba646b1a5d1c4cbe0cf897b"
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettospot-yp2lqjzcg6l.ws-eu117.gitpod.io/callback"

sp_oauth = SpotifyOAuth (
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private",
    show_dialog=True
)

def get_spotify_object(token_info):
    return spotipy.Spotify(auth=token_info['access_token'])