from flask import Flask
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.home import home_bp
from blueprints.search import search_bp
from blueprints.analizza import analizza_bp
from blueprints.local_login import local_login_bp
from blueprints.compara import compara_bp
from services.models import User  # Importa la classe User per gestire gli utenti
from blueprints.salva_playlist_locale import salva_playlist_bp

# Crea un'istanza dell'app Flask
app = Flask(__name__)

# Imposta la chiave segreta per la sessione, utilizzata per gestire i cookie sicuri
app.secret_key = 'chiave_per_session'

# Configura il LoginManager per gestire l'autenticazione degli utenti
login_manager = LoginManager()
login_manager.init_app(app)  # Inizializza il LoginManager con l'app Flask
login_manager.login_view = 'local_login.login_page'  # Imposta la vista di login predefinita

# Funzione per caricare l'utente tramite il suo ID
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)  # Recupera l'utente dal database usando l'ID

# Registra i Blueprint per modularizzare l'app e gestire diverse funzionalità
app.register_blueprint(local_login_bp)  # Blueprint per il login locale
app.register_blueprint(auth_bp)  # Blueprint per la gestione dell'autenticazione
app.register_blueprint(home_bp)  # Blueprint per la home page
app.register_blueprint(search_bp)  # Blueprint per la ricerca
app.register_blueprint(analizza_bp)  # Blueprint per l'analisi delle playlist
app.register_blueprint(salva_playlist_bp)  # Blueprint per il salvataggio delle playlist locali
app.register_blueprint(compara_bp)  # Blueprint per il confronto delle playlist

# Avvia il server Flask in modalità di debug (per sviluppo)
if __name__ == '__main__':
    app.run(debug=True)
