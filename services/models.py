import pymysql

class DatabaseWrapper:
    
    #costruttore ogg db
    def __init__(self, host, user, password, database):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'cursorclass': pymysql.cursors.DictCursor  #restituisce i risultati come dizionario
        }
        self.create_table()  #creazione della tabella all'avvio

    #connessione al db
    def connect(self):
        return pymysql.connect(**self.db_config)

    #fa le operazioni di DML e DDL
    def execute_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
        conn.close()

    #per eseguire le select (fa le operazioni di DQL)
    def fetch_query(self, query, params=()):
        conn = self.connect()
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
        conn.close()
        return result #restituisce il risultato delle select

        def create_table_Utente(self):
            self.execute_query('''
            CREATE TABLE IF NOT EXISTS Utente (
                id_u INT AUTO_INCREMENT PRIMARY KEY,
                nickname VARCHAR(100) NOT NULL,
                password VARCHAR(100) NOT NULL,
                
            )
        ''')
        
        def create_table_playlist(self):
            self.execute_query('''
            CREATE TABLE IF NOT EXISTS Playlist (
                id_p VARCHAR(255) PRIMARY KEY,
                id_u INT NOT NULL,
                
            )
        ''')
    def get_Utente(self):
        return self.fetch_query('SELECT * FROM Utente')
    
    def get_Playlist(self):
        return self.fetch_query('SELECT * FROM Playlist')


    #manipolazione tabelle con execute_query!!!!
    def aggiungi_Utente(self, nickname, password):
        self.execute_query('INSERT INTO Utente (nickname, password) VALUES (%s)', (nickname, password,))
        
    def aggiungi_Playlist(self, nickname, password):
        self.execute_query('INSERT INTO Utente (nickname, password) VALUES (%s)', (nickname, password,))
        
        
    #%s fa da placeholder: "la variabile che passo come parametro prende il valore di %s"

    def rimuovi_Playlist(self, indice):
        self.execute_query('DELETE FROM Playlist WHERE id_p = %s', (indice,))

    def rimuovi_Utente(self, indice):
        self.execute_query('DELETE FROM Utente WHERE id_u = %s', (indice,))

    def svuota_Utente(self):
        self.execute_query('DELETE FROM Utente')

    def svuota_Playlist(self):
        self.execute_query('DELETE FROM Playlist')


