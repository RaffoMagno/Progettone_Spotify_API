from flask import Blueprint, request, render_template, session, redirect, url_for
from services.analyse import analizza_playlist
import spotipy

analizza_bp = Blueprint('analizza', __name__)

@analizza_bp.route('/analizza/<playlist_id>')
def analizza_playlist_view(playlist_id):
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('auth.login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks = sp.playlist_tracks(playlist_id)['items']

    playlist = sp.playlist(playlist_id)  
    tracks = playlist['tracks']['items']
    playlist_name = playlist['name']
    
    # Passiamo i brani al servizio di analisi
    plots = analizza_playlist(tracks)

    return render_template('brani.html', playlist_name=playlist_name, tracks=tracks, plots=plots)