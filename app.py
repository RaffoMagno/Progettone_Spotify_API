from flask import Flask
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.home import home_bp
from blueprints.search import search_bp
from blueprints.analizza import analizza_bp
from blueprints.local_login import local_login_bp
from services.models import User  # Importa la classe User

app = Flask(__name__)
app.secret_key = 'chiave_per_session'  # Imposta la chiave segreta per la sessione

# Configura il LoginManager
login_manager = LoginManager()
login_manager.init_app(app)  # Associa il LoginManager all'app Flask

# Imposta il percorso di login
login_manager.login_view = 'local_login.login_page'  # Modifica con il nome corretto del percorso di login

# Funzione per caricare un utente
@login_manager.user_loader
def load_user(user_id):
    # Usa la funzione User.get() che abbiamo definito in precedenza
    return User.get(user_id)  # user_id è il nickname dell'utente

# Registriamo i Blueprint
app.register_blueprint(local_login_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(search_bp)
app.register_blueprint(analizza_bp)

if __name__ == '__main__':
    app.run(debug=True)
