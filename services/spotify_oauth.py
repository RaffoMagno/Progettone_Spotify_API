import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

SPOTIFY_CLIENT_ID = "f726b08700854dd8997d401bdb42894b"
SPOTIFY_CLIENT_SECRET = "7fb5909e43b244099dfed6689cf4ef9f"
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettonesp-ekpgstao5pv.ws-eu118.gitpod.io/callback" #ognuno qui inserisce il proprio link seguito da "/callback"
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