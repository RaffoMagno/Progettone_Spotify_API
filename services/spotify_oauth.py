import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

SPOTIFY_CLIENT_ID = "b1ed2d5909a24d66912adc6f42531fee"
SPOTIFY_CLIENT_SECRET = "db711b1f9ba646b1a5d1c4cbe0cf897b"
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettonesp-72o7xu40jhr.ws-eu118.gitpod.io/callback"
SPOTIFY_SCOPE = "user-read-private user-read-email playlist-read-private"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE,
    show_dialog=True
)

# Autenticazione pubblica per chi non ha fatto login
sp_public = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Funzione per ottenere l'oggetto Spotify corretto
def get_spotify_object(token_info=None):
    if token_info:
        return spotipy.Spotify(auth=token_info['access_token'])
    return sp_public  # Accesso limitato per utenti non autenticati