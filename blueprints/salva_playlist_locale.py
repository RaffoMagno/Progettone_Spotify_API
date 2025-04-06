from flask import Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required
from services.models import db

salva_playlist_bp = Blueprint('salva_playlist', __name__)

@salva_playlist_bp.route('/salva_playlist/<playlist_id>', methods=['POST'])
@login_required
def salva_playlist(playlist_id):
    if not current_user.is_authenticated:
        flash("Effettua l’accesso locale per salvare la playlist", "error")
        return redirect(url_for('home.homepage'))

    db.aggiungi_Playlist(playlist_id, current_user.nickname)
    flash("Playlist salvata correttamente!", "success")
    return redirect(request.referrer or url_for('home.homepage'))