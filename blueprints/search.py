from flask import Blueprint, request, render_template, flash
import spotipy
from services.spotify_oauth import SpotifyClientCredentials, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Crea il Blueprint per la ricerca delle playlist
search_bp = Blueprint('search', __name__)

# Creiamo un'istanza di Spotipy utilizzando le credenziali client
# Questa istanza permette di fare richieste a Spotify senza bisogno di autenticazione utente
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

# Rotta per la ricerca delle playlist
@search_bp.route('/search')
def search():
    # Otteniamo la query di ricerca passata come parametro GET nella URL
    query = request.args.get('query')
    
    # Se la query è vuota, restituiamo la pagina di ricerca senza risultati
    if not query:
        return render_template('search.html', results=None)

    # Altrimenti, eseguiamo la ricerca su Spotify per le playlist
    # Limitiamo il numero di risultati a 10
    results = sp.search(q=query, type='playlist', limit=10)
    
    # Otteniamo le playlist dai risultati della ricerca
    playlists = results['playlists']['items']

    # Passiamo i risultati alla pagina di template per visualizzarli
    return render_template('search.html', query=query, results=playlists)

# Rotta per ottenere i brani di una playlist
@search_bp.route('/playlist/<playlist_id>')
def get_playlist_tracks(playlist_id):
    """Ottiene i brani di una playlist e li mostra in una tabella sotto la playlist."""
    
    # Otteniamo i brani della playlist usando l'ID della playlist
    tracks = sp.playlist_tracks(playlist_id)['items']
    
    # Passiamo la lista dei brani al template per visualizzarli
    return render_template('playlist_tracks.html', tracks=tracks)
