import sqlite3
import os

class DatabaseWrapper:
    def __init__(self, db_file='SpotifyDB.db'):
        # Inizializza il percorso del file del database SQLite
        # Se non viene fornito un percorso, usa il file 'SpotifyDB.db' nella cartella di progetto
        self.db_file = db_file
        self.create_tables()  # Crea le tabelle all'avvio, se non esistono già

    def connect(self):
        # Crea una connessione al database SQLite
        return sqlite3.connect(self.db_file)

    def execute_query(self, query, params=()):
        # Esegui una query di modifica (INSERT, UPDATE, DELETE) sul database
        conn = self.connect()
        with conn:
            cursor = conn.cursor()
            cursor.execute(query, params)  # Esegui la query con i parametri forniti
            conn.commit()  # Salva le modifiche nel database

    def fetch_query(self, query, params=()):
        # Esegui una query di selezione (SELECT) e restituisci i risultati
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)  # Esegui la query con i parametri forniti
        result = cursor.fetchall()  # Ottieni tutti i risultati della query
        conn.close()  # Chiudi la connessione al database
        return result

    def create_tables(self):
        # Crea tutte le tabelle necessarie nel database
        self.create_table_Utente()  # Crea la tabella 'Utente'
        self.create_table_playlist()  # Crea la tabella 'Playlist'

    def create_table_Utente(self):
        # Crea la tabella 'Utente' se non esiste
        self.execute_query(''' 
            CREATE TABLE IF NOT EXISTS Utente (
                nickname TEXT NOT NULL UNIQUE,  # Il nickname è un campo obbligatorio e unico
                password TEXT NOT NULL,  # La password è obbligatoria
                PRIMARY KEY (nickname)  # Imposta il nickname come chiave primaria
            )
        ''')

    def create_table_playlist(self):
        # Crea la tabella 'Playlist' se non esiste
        self.execute_query(''' 
        CREATE TABLE IF NOT EXISTS Playlist (
            id_p TEXT,  # Identificativo della playlist
            nickname TEXT NOT NULL,  # Il nickname dell'utente che ha creato la playlist
            PRIMARY KEY (id_p, nickname),  # La combinazione di id_p e nickname è unica
            FOREIGN KEY (nickname) REFERENCES Utente(nickname) ON DELETE CASCADE  # La chiave esterna fa riferimento alla tabella 'Utente'
        )
    ''')

    def get_Utente(self):
        # Recupera tutti gli utenti dal database
        return self.fetch_query('SELECT * FROM Utente')

    def get_Playlist(self):
        # Recupera tutte le playlist dal database
        return self.fetch_query('SELECT * FROM Playlist')

    def aggiungi_Utente(self, nickname, password):
        # Aggiungi un nuovo utente al database
        self.execute_query('INSERT INTO Utente (nickname, password) VALUES (?, ?)', (nickname, password))

    def aggiungi_Playlist(self, id_p, nickname):
        # Aggiungi una nuova playlist al database (ignorando duplicati)
        self.execute_query('INSERT OR IGNORE INTO Playlist (id_p, nickname) VALUES (?, ?)', (id_p, nickname))

    def rimuovi_Playlist(self, id_p):
        # Rimuovi una playlist dal database in base al suo id
        self.execute_query('DELETE FROM Playlist WHERE id_p = ?', (id_p,))

    def rimuovi_Utente(self, indice):
        # Rimuovi un utente dal database in base al suo indice
        self.execute_query('DELETE FROM Utente WHERE id_u = ?', (indice,))

    def svuota_Utente(self):
        # Svuota la tabella 'Utente', rimuovendo tutti gli utenti
        self.execute_query('DELETE FROM Utente')

    def svuota_Playlist(self):
        # Svuota la tabella 'Playlist', rimuovendo tutte le playlist
        self.execute_query('DELETE FROM Playlist')

# Crea un'istanza del wrapper del database
# Non creare l'istanza dentro la classe, ma fuori per mantenerla globale
db = DatabaseWrapper(db_file="SpotifyDB.db")  # Crea un'istanza del database usando il file 'SpotifyDB.db'

from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, nickname):
        # Inizializza l'oggetto utente con un nickname
        self.nickname = nickname

    @staticmethod
    def get(user_id):
        # Recupera un utente dal database utilizzando il suo nickname (user_id)
        utenti = db.get_Utente()  # Ottieni tutti gli utenti dal database
        user_data = next((u for u in utenti if u[0] == user_id), None)  # Trova l'utente con il nickname corrispondente
        if user_data:
            return User(nickname=user_data[0])  # Restituisci un'istanza di User con il nickname trovato
        return None

    def get_id(self):
        # Restituisce l'identificativo dell'utente, che è il nickname
        return self.nickname
