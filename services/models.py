import sqlite3
import os

class DatabaseWrapper:
    
    def __init__(self, db_name="SpotifyDB.sqlite"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def execute_query(self, query, params=()):
        conn = self.connect()
        with conn:
            conn.execute(query, params)
        conn.close()

    def fetch_query(self, query, params=()):
        conn = self.connect()
        with conn:
            cursor = conn.execute(query, params)
            result = cursor.fetchall()
        conn.close()
        return result

    def create_tables(self):
        self.create_table_Utente()
        self.create_table_playlist()

    def create_table_Utente(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS Utente (
                id_u INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')

    def create_table_playlist(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS Playlist (
                id_p TEXT PRIMARY KEY,
                id_u INTEGER NOT NULL,
                FOREIGN KEY (id_u) REFERENCES Utente(id_u) ON DELETE CASCADE
            )
        ''')

    def get_Utente(self):
        return self.fetch_query('SELECT * FROM Utente')

    def get_Playlist(self):
        return self.fetch_query('SELECT * FROM Playlist')

    def aggiungi_Utente(self, nickname, password):
        self.execute_query('INSERT INTO Utente (nickname, password) VALUES (?, ?)', (nickname, password))

    def aggiungi_Playlist(self, id_p, id_u):
        self.execute_query('INSERT INTO Playlist (id_p, id_u) VALUES (?, ?)', (id_p, id_u))

    def rimuovi_Playlist(self, id_p):
        self.execute_query('DELETE FROM Playlist WHERE id_p = ?', (id_p,))

    def rimuovi_Utente(self, id_u):
        self.execute_query('DELETE FROM Utente WHERE id_u = ?', (id_u,))

    def svuota_Utente(self):
        self.execute_query('DELETE FROM Utente')

    def svuota_Playlist(self):
        self.execute_query('DELETE FROM Playlist')