from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from services.models import db

# Crea il Blueprint per la gestione delle playlist salvate
salva_playlist_bp = Blueprint('salva_playlist', __name__)

# Route per salvare una playlist
@salva_playlist_bp.route('/salva_playlist/<playlist_id>', methods=['POST'])
@login_required  # Questa rotta è protetta: solo gli utenti autenticati possono accedervi
def salva_playlist(playlist_id):
    # Se l'utente non è autenticato, mostra un errore e reindirizza alla homepage
    if not current_user.is_authenticated:
        flash("Effettua l’accesso locale per salvare la playlist", "error")
        return redirect(url_for('home.homepage'))

    # Se l'utente è autenticato, salva la playlist nel database associandola al suo nickname
    db.aggiungi_Playlist(playlist_id, current_user.nickname)
    flash("Playlist salvata correttamente!", "success")  # Messaggio di conferma

    # Dopo aver salvato la playlist, reindirizza l'utente alla pagina precedente
    return redirect(request.referrer or url_for('home.homepage'))
