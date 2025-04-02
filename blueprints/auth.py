from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import logout_user
from services.spotify_oauth import sp_oauth
import spotipy

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/logout_spotify')
def logout_spotify():
    session.pop('token_info', None)
    session.pop('spotify_username', None)
    flash("Sei tornato all'utente locale!", "success")
    return redirect(url_for('home.homepage'))

@auth_bp.route('/logout_local')
def logout_local():
    logout_user()  # Termina la sessione locale
    flash("Logout effettuato!", "success")
    return redirect(url_for('local_login.login_page'))  # Redirige alla pagina di login locale

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info

    # Ottenere informazioni sull'utente Spotify
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    session['spotify_username'] = user_info.get('display_name', 'Utente Spotify')

    return redirect(url_for('home.homepage'))