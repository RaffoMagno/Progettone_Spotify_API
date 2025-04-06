from flask import Blueprint, redirect, request, url_for, session, render_template, flash
from flask_login import current_user
import spotipy
from services.models import db
from services.spotify_oauth import get_spotify_object, SpotifyClientCredentials, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, sp_public

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def homepage():
    token_info = session.get('token_info', None)
    sp = get_spotify_object(token_info) if token_info else sp_public
    if token_info:
        sp = get_spotify_object(token_info)
        user_info = sp.current_user()
        playlists = sp.current_user_playlists()['items']
    else:
        user_info = None
        saved_playlists = db.fetch_query('SELECT * FROM Playlist WHERE nickname = ?', (current_user.nickname,))
        playlists = []
        for saved_playlist in saved_playlists:
            playlist_id = saved_playlist[0]  # id_p della playlist salvata
            # Recupera i dettagli della playlist tramite l'API di Spotify
            playlist_details = sp.playlist(playlist_id)
            playlists.append(playlist_details)

    return render_template('home.html', user_info=user_info, playlists=playlists)

@home_bp.route('/remove_playlist/<playlist_id>', methods=['POST'])
def remove_playlist(playlist_id):
    if not current_user.is_authenticated:
        return redirect(url_for('home.homepage'))
    
    # Rimuovi la playlist dal database
    db.rimuovi_Playlist(playlist_id)
    
    flash("Playlist rimossa correttamente.", "success")
    return redirect(url_for('home.homepage'))

@home_bp.route('/visualizza_brani/<playlist_id>')
def visualizza_brani(playlist_id):
    token_info = session.get('token_info', None)
    sp = get_spotify_object(token_info) if token_info else sp_public
    
    # Ottenere i dettagli della playlist per estrarre il nome
    playlist = sp.playlist(playlist_id)  
    tracks = playlist['tracks']['items']
    playlist_name = playlist['name']

    return render_template('brani.html', tracks=tracks, playlist_name=playlist_name)