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
    
    recommendations = []  # Lista vuota per i brani consigliati

    # Se l'utente è autenticato con Spotify
    if token_info:
        user_info = sp.current_user()
        playlists = sp.current_user_playlists()['items']

        # Recupera i brani consigliati solo se l'utente ha playlist
        if playlists:
            first_playlist_id = playlists[0]['id']
            try:
                # Recupera i brani della prima playlist
                playlist_tracks = sp.playlist_tracks(first_playlist_id, limit=10)['items']
                seed_tracks = [track['track']['id'] for track in playlist_tracks if track.get('track')]

                # Prendi al massimo 5 seed track id
                seed_tracks = seed_tracks[:5]  

                # Se sono disponibili seed track, richiedi raccomandazioni
                if seed_tracks:
                    recs = sp.recommendations(seed_tracks=seed_tracks, limit=9)
                    recommendations = recs['tracks']
            except Exception as e:
                print(f"Errore durante il recupero delle raccomandazioni: {e}")

    else:
        # Se l'utente non è autenticato con Spotify, carica le playlist salvate localmente
        user_info = None
        saved_playlists = db.fetch_query('SELECT * FROM Playlist WHERE nickname = ?', (current_user.nickname,))
        playlists = []

        for saved_playlist in saved_playlists:
            playlist_id = saved_playlist[0]
            playlist_details = sp.playlist(playlist_id)
            playlists.append(playlist_details)

    # Restituisci il template 'home.html' con user_info, playlists e recommendations
    return render_template('home.html', user_info=user_info, playlists=playlists, recommendations=recommendations)

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
