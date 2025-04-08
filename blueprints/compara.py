from flask import Blueprint, request, render_template
from services.compare import confronta_playlist

compara_bp = Blueprint('compara', __name__)

@compara_bp.route('/compara')
def compara_view():
    playlist1 = request.args.get('p1')
    playlist2 = request.args.get('p2')

    if not playlist1 or not playlist2:
        return "Playlist mancanti", 400

    dati = confronta_playlist(playlist1, playlist2)
    return render_template('compara.html', **dati)