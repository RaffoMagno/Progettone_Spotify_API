import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configura l'autenticazione per l'API di Spotify
# Viene usato un OAuth per autenticare e autorizzare l'accesso all'account Spotify dell'utente
# Sostituisci "YOUR_CLIENT_ID", "YOUR_CLIENT_SECRET", e "YOUR_REDIRECT_URI" con i valori corretti
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="YOUR_REDIRECT_URI",
                                               scope="user-library-read"))  # L'ambito 'user-library-read' consente l'accesso alla libreria dell'utente

def get_playlist_tracks(playlist_id):
    """
    Recupera tutte le tracce di una playlist usando l'API di Spotify.
    Gestisce la paginazione per recuperare tutte le tracce, anche se la playlist è lunga.
    """
    results = sp.playlist_tracks(playlist_id)  # Ottieni le tracce della playlist dalla API di Spotify
    tracks = results['items']  # Estrai le tracce dalla risposta JSON
    
    # Spotify fornisce solo una parte dei risultati alla volta, quindi se la playlist è lunga, usiamo la paginazione
    while results['next']:  # Finché ci sono altre pagine di risultati
        results = sp.next(results)  # Ottieni la pagina successiva
        tracks.extend(results['items'])  # Aggiungi le tracce della pagina successiva alla lista totale
    
    return tracks  # Restituisce tutte le tracce raccolte dalla playlist
