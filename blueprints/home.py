from flask import Blueprint, redirect, request, url_for, session, render_template, flash
from flask_login import current_user
import spotipy
from services.models import db
from services.spotify_oauth import get_spotify_object, SpotifyClientCredentials, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, sp_public

# Crea il Blueprint per la sezione 'home' dell'applicazione
home_bp = Blueprint('home', __name__)

# Route per la homepage dell'utente
@home_bp.route('/home')
def homepage():
    # Recupera le informazioni sul token di accesso dalla sessione (se presente)
    token_info = session.get('token_info', None)
    
    # Crea un oggetto Spotify utilizzando il token di accesso, se disponibile
    sp = get_spotify_object(token_info) if token_info else sp_public
    
    # Se l'utente è autenticato, recupera le informazioni dell'utente e le sue playlist da Spotify
    if token_info:
        user_info = sp.current_user()  # Ottieni informazioni sull'utente corrente da Spotify
        playlists = sp.current_user_playlists()['items']  # Recupera le playlist dell'utente
    else:
        # Se l'utente non è autenticato, carica le playlist salvate localmente dal database
        user_info = None  # Nessuna informazione utente, perché l'utente non è loggato
        saved_playlists = db.fetch_query('SELECT * FROM Playlist WHERE nickname = ?', (current_user.nickname,))
        playlists = []
        
        # Per ogni playlist salvata, recupera i dettagli tramite l'API di Spotify
        for saved_playlist in saved_playlists:
            playlist_id = saved_playlist[0]  # ID della playlist salvata
            playlist_details = sp.playlist(playlist_id)  # Ottieni i dettagli della playlist tramite l'API Spotify
            playlists.append(playlist_details)  # Aggiungi i dettagli alla lista delle playlist

    # Restituisci il template 'home.html' con le informazioni utente e playlist
    return render_template('home.html', user_info=user_info, playlists=playlists)

# Route per rimuovere una playlist dal database
@home_bp.route('/remove_playlist/<playlist_id>', methods=['POST'])
def remove_playlist(playlist_id):
    # Verifica se l'utente è autenticato prima di permettere l'operazione
    if not current_user.is_authenticated:
        return redirect(url_for('home.homepage'))  # Se non è autenticato, reindirizza alla homepage
    
    # Rimuovi la playlist dal database
    db.rimuovi_Playlist(playlist_id)
    
    # Mostra un messaggio di successo
    flash("Playlist rimossa correttamente.", "success")
    
    # Reindirizza di nuovo alla homepage
    return redirect(url_for('home.homepage'))

# Route per visualizzare i brani di una playlist
@home_bp.route('/visualizza_brani/<playlist_id>')
def visualizza_brani(playlist_id):
    # Recupera le informazioni sul token di accesso dalla sessione (se presente)
    token_info = session.get('token_info', None)
    sp = get_spotify_object(token_info) if token_info else sp_public  # Crea un oggetto Spotify
    
    # Ottieni i dettagli della playlist selezionata
    playlist = sp.playlist(playlist_id)  
    tracks = playlist['tracks']['items']  # Ottieni i brani dalla playlist
    playlist_name = playlist['name']  # Ottieni il nome della playlist

    # Restituisci il template 'brani.html' con i dettagli della playlist e i brani
    return render_template('brani.html', tracks=tracks, playlist_name=playlist_name)
