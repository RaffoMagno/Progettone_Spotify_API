import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

def plot_to_base64(fig):
    """Converte un grafico Matplotlib in una stringa Base64 per l'HTML."""
    img = io.BytesIO()
    fig.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def analizza_playlist(tracks):
    """Analizza i brani della playlist e genera statistiche e grafici."""
    if not tracks:
        return {}

    # DataFrame con artisti e album
    data = []
    for track in tracks:
        track_info = track.get('track', {})
        if not track_info:
            continue
        artists = [artist['name'] for artist in track_info.get('artists', [])]
        album = track_info.get('album', {}).get('name', 'Sconosciuto')
        genres = track_info.get('album', {}).get('genres', [])  # Potrebbe essere vuoto
        data.append({'title': track_info['name'], 'artist': ', '.join(artists), 'album': album, 'genres': ', '.join(genres)})

    df = pd.DataFrame(data)

    plots = {}

    # 5 Artisti più presenti
    artist_count = df['artist'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(artist_count.index, artist_count.values, color='purple')
    ax.set_title('Top 5 Artisti più Presenti')
    ax.set_xlabel('Numero di Brani')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plots['top_artists'] = plot_to_base64(fig)

    # 5 Album più presenti
    album_count = df['album'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(album_count.index, album_count.values, color='orange')
    ax.set_title('Top 5 Album più Presenti')
    ax.set_xlabel('Numero di Brani')
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plots['top_albums'] = plot_to_base64(fig)

    # Distribuzione Generi Musicali (se disponibili)
    if not df['genres'].isna().all():
        genre_list = df['genres'].str.split(', ').explode().dropna()
        genre_count = genre_list.value_counts().head(7)
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.barh(genre_count.index, genre_count.values, color='red')
        ax.set_title('Distribuzione Generi Musicali')
        ax.set_xlabel('Numero di Brani')
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        plots['top_genres'] = plot_to_base64(fig)

    # Numero di brani per artista (aggiunta extra)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.pie(artist_count, labels=artist_count.index, autopct=lambda p: f'{int(p * artist_count.sum() / 100)}%', startangle=90, colors=['blue', 'green', 'red', 'purple', 'orange'])
    ax.set_title('Distribuzione Brani per Artista')
    plots['artist_distribution'] = plot_to_base64(fig)

    return plots