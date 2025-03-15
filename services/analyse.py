import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

    # Creiamo un DataFrame con gli artisti e gli album
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

    # 🔹 1. Top 5 Artisti più presenti
    artist_count = df['artist'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=artist_count.values, y=artist_count.index, ax=ax, palette='viridis')
    ax.set_title('Top 5 Artisti più Presenti')
    plots['top_artists'] = plot_to_base64(fig)

    # 🔹 2. Top 5 Album più presenti
    album_count = df['album'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=album_count.values, y=album_count.index, ax=ax, palette='magma')
    ax.set_title('Top 5 Album più Presenti')
    plots['top_albums'] = plot_to_base64(fig)

    # 🔹 3. Distribuzione Generi Musicali (se disponibili)
    if not df['genres'].isna().all():
        genre_list = df['genres'].str.split(', ').explode().dropna()
        genre_count = genre_list.value_counts().head(7)
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=genre_count.values, y=genre_count.index, ax=ax, palette='coolwarm')
        ax.set_title('Distribuzione Generi Musicali')
        plots['top_genres'] = plot_to_base64(fig)

    # 🔹 4. Numero di brani per artista (aggiunta extra)
    fig, ax = plt.subplots(figsize=(6, 4))
    artist_count.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, cmap='Set3')
    ax.set_ylabel('')
    ax.set_title('Distribuzione Brani per Artista')
    plots['artist_distribution'] = plot_to_base64(fig)

    return plots