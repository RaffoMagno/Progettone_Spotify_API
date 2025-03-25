import pymysql

class DatabaseWrapper:
    
    def __init__(self, host, user, password, database):
        self.db_config = {
            'host': "localhost",
            'user': "root",
            'password': "password",
            'database': "SpotifyDB",
        }
        self.create_tables()  # Creazione delle tabelle all'avvio

    def connect(self):
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        conn.close()

    def fetch_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        conn.close()
        return result

    def create_tables(self):
        self.create_table_Utente()
        self.create_table_playlist()

    def create_table_Utente(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS Utente (
                id_u INT AUTO_INCREMENT PRIMARY KEY,
                nickname VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(100) NOT NULL
            )
        ''')

    def create_table_playlist(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS Playlist (
                id_p VARCHAR(255) PRIMARY KEY,
                id_u INT NOT NULL,
                FOREIGN KEY (id_u) REFERENCES Utente(id_u) ON DELETE CASCADE
            )
        ''')

    def get_Utente(self):
        return self.fetch_query('SELECT * FROM Utente')

    def get_Playlist(self):
        return self.fetch_query('SELECT * FROM Playlist')

    def aggiungi_Utente(self, nickname, password):
        self.execute_query('INSERT INTO Utente (nickname, password) VALUES (%s, %s)', (nickname, password,))

    def aggiungi_Playlist(self, id_p, id_u):
        self.execute_query('INSERT INTO Playlist (id_p, id_u) VALUES (%s, %s)', (id_p, id_u,))

    def rimuovi_Playlist(self, indice):
        self.execute_query('DELETE FROM Playlist WHERE id_p = %s', (indice,))

    def rimuovi_Utente(self, indice):
        self.execute_query('DELETE FROM Utente WHERE id_u = %s', (indice,))

    def svuota_Utente(self):
        self.execute_query('DELETE FROM Utente')

    def svuota_Playlist(self):
        self.execute_query('DELETE FROM Playlist')
