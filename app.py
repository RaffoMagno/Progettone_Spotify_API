from flask import Flask
from flask_login import LoginManager
from blueprints.auth import auth_bp
from blueprints.home import home_bp
from blueprints.search import search_bp
from blueprints.analizza import analizza_bp
from blueprints.local_login import local_login_bp
from blueprints.compara import compara_bp
from services.models import User  # Importa la classe User
from blueprints.salva_playlist_locale import salva_playlist_bp

app = Flask(__name__)
app.secret_key = 'chiave_per_session'  # Imposta la chiave segreta per la sessione

# Configura il LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'local_login.login_page'

# Funzione per caricare un utente
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Registriamo i Blueprint
app.register_blueprint(local_login_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(search_bp)
app.register_blueprint(analizza_bp)
app.register_blueprint(salva_playlist_bp)
app.register_blueprint(compara_bp)

if __name__ == '__main__':
    app.run(debug=True)