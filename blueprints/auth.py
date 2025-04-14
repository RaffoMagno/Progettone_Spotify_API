# Importazione dei moduli necessari di Flask, Flask-Login e dei servizi personalizzati
from flask import Blueprint, redirect, request, url_for, session, flash
from flask_login import logout_user
from services.spotify_oauth import sp_oauth  # Oggetto di autenticazione con Spotify
import spotipy  # Libreria ufficiale per interagire con le API di Spotify

# Creazione del Blueprint per gestire le rotte di autenticazione
auth_bp = Blueprint('auth', __name__)

# Rotta per avviare il login con Spotify
@auth_bp.route('/login')
def login():
    # Otteniamo l'URL di autorizzazione da Spotify e reindirizziamo l'utente
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

# Rotta per disconnettere l'utente da Spotify
@auth_bp.route('/logout_spotify')
def logout_spotify():
    # Rimuove le informazioni di sessione relative a Spotify
    session.pop('token_info', None)
    session.pop('spotify_username', None)
    # Mostra un messaggio di conferma
    flash("Sei tornato all'utente locale!", "success")
    # Reindirizza alla homepage
    return redirect(url_for('home.homepage'))

# Rotta per effettuare il logout dell'utente locale (gestito da Flask-Login)
@auth_bp.route('/logout_local')
def logout_local():
    logout_user()  # Termina la sessione utente locale
    flash("Logout effettuato!", "success")
    return redirect(url_for('local_login.login_page'))  # Redirige alla pagina di login locale

# Rotta di callback chiamata da Spotify dopo il login
@auth_bp.route('/callback')
def callback():
    # Recuperiamo il codice inviato da Spotify come parametro nella richiesta
    code = request.args.get('code')

    # Otteniamo il token di accesso utilizzando il codice
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info  # Salviamo le informazioni del token nella sessione

    # Usiamo il token per ottenere i dati dell'utente Spotify
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.current_user()
    
    # Salviamo il nome visualizzato dell'utente nella sessione, se disponibile
    session['spotify_username'] = user_info.get('display_name', 'Utente Spotify')

    # Redirigiamo alla homepage
    return redirect(url_for('home.homepage'))
