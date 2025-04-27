import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

# Le credenziali di Spotify per l'autenticazione
# Sostituisci questi valori con le tue credenziali (client_id, client_secret, e redirect_uri)
SPOTIFY_CLIENT_ID = "6cdc57044c7e4a4eacc20754b6fd038b"  # Non cambiare questo campo
SPOTIFY_CLIENT_SECRET = "16b492cf1a764f5d9756e33db66a990e"  # Non cambiare questo campo
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettonesp-ekpgstao5pv.ws-eu118.gitpod.io/callback"  # Inserisci il tuo redirect URI seguito da "/callback"
SPOTIFY_SCOPE = "user-read-private user-read-email playlist-read-private"  # Permessi per l'accesso ai dati utente e playlist

# Impostazione dell'autenticazione con OAuth per l'accesso tramite account utente
sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE,
    show_dialog=True  # Mostra la finestra di login dell'utente
)

# Autenticazione pubblica per chi non ha effettuato il login, con credenziali client
# Questo fornisce accesso limitato (non richiede un login utente)
sp_public = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Funzione per ottenere l'oggetto Spotify corretto in base alla presenza di un token
def get_spotify_object(token_info=None):
    """
    Restituisce un oggetto Spotify autenticato con il token dell'utente (se fornito),
    altrimenti restituisce un oggetto con accesso pubblico limitato.
    """
    if token_info:
        # Se sono presenti informazioni sul token (utente autenticato), restituisci un oggetto Spotify autenticato
        return spotipy.Spotify(auth=token_info['access_token'])
    return sp_public  # Restituisce l'oggetto per l'accesso pubblico (per utenti non autenticati)
