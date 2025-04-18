from flask import Blueprint, request, render_template, flash
import spotipy
from services.spotify_oauth import SpotifyClientCredentials, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

search_bp = Blueprint('search', __name__)

# abbiamo creato  un'istanza Spotipy con credenziali client (senza login utente)
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

@search_bp.route('/search')
def search():
    query = request.args.get('query')
    if not query:
        return render_template('search.html', results=None)

    results = sp.search(q=query, type='playlist', limit=10)
    playlists = results['playlists']['items']

    return render_template('search.html', query=query, results=playlists)



@search_bp.route('/playlist/<playlist_id>')
def get_playlist_tracks(playlist_id):
    """Ottiene i brani di una playlist e li mostra in una tabella sotto la playlist."""
    tracks = sp.playlist_tracks(playlist_id)['items']
    return render_template('playlist_tracks.html', tracks=tracks)