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