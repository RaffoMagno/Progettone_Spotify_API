from flask import Blueprint, render_template, request, jsonify
from services.spotify_api import get_playlist_tracks
from collections import Counter
import matplotlib.pyplot as plt
import io
import base64
from flask import send_file
from io import BytesIO
from datetime import datetime

analizza_bp = Blueprint('analizza', __name__)

def get_release_years(tracks):
    """
    Estrae le date di rilascio dei brani e aggrega i dati per anno.
    """
    release_years = []
    for track in tracks:
        # Ottieni la data di rilascio della traccia
        release_date = track['track']['album']['release_date']
        release_year = datetime.strptime(release_date, '%Y-%m-%d').year
        release_years.append(release_year)
    
    # Conta la frequenza dei brani per ogni anno
    year_counts = Counter(release_years)
    return year_counts

def generate_release_year_chart(years_playlist_1, years_playlist_2):
    """
    Genera un grafico a barre che mostra la distribuzione dei brani per anno tra due playlist.
    """
    years_1, counts_1 = zip(*years_playlist_1.items()) if years_playlist_1 else ([], [])
    years_2, counts_2 = zip(*years_playlist_2.items()) if years_playlist_2 else ([], [])

    fig, ax = plt.subplots()

    # Creiamo un grafico a barre per confrontare i due set di dati
    ax.bar(years_1, counts_1, width=0.4, label='Playlist 1', align='center')
    ax.bar(years_2, counts_2, width=0.4, label='Playlist 2', align='edge')

    ax.set_xlabel('Anno di Rilascio')
    ax.set_ylabel('Frequenza dei Brani')
    ax.set_title('Distribuzione Temporale dei Brani tra Playlist 1 e Playlist 2')
    ax.legend()

    # Salviamo il grafico in un oggetto BytesIO per poterlo visualizzare nel template
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return img

@analizza_bp.route('/confronta_temporale/<playlist_id_1>/<playlist_id_2>', methods=['GET'])
def confronta_temporalmente_playlist(playlist_id_1, playlist_id_2):
    """
    Visualizza il confronto della distribuzione temporale dei brani tra due playlist.
    """
    # Recupera le tracce delle playlist
    playlist_1_tracks = get_playlist_tracks(playlist_id_1)
    playlist_2_tracks = get_playlist_tracks(playlist_id_2)
    
    # Estrai la distribuzione temporale dei brani per entrambe le playlist
    years_playlist_1 = get_release_years(playlist_1_tracks)
    years_playlist_2 = get_release_years(playlist_2_tracks)
    
    # Genera il grafico a barre
    img = generate_release_year_chart(years_playlist_1, years_playlist_2)
    
    # Converti l'immagine in un formato che può essere visualizzato nel template
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    return render_template('confronta_temporale.html', img_base64=img_base64, 
                           years_playlist_1=years_playlist_1, years_playlist_2=years_playlist_2,
                           playlist_id_1=playlist_id_1, playlist_id_2=playlist_id_2)
