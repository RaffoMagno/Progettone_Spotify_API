import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Configura l'autenticazione per l'API di Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="YOUR_CLIENT_ID",
                                               client_secret="YOUR_CLIENT_SECRET",
                                               redirect_uri="YOUR_REDIRECT_URI",
                                               scope="user-library-read"))

def get_playlist_tracks(playlist_id):
    """
    Recupera tutte le tracce di una playlist usando l'API di Spotify.
    """
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Spotify fornisce solo una parte dei risultati, se la playlist è lunga, possiamo fare paginazione
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    return tracks
