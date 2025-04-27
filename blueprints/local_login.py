from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
import re  # Import necessario per controllare la validità della password

# Crea il Blueprint per la sezione di login locale
local_login_bp = Blueprint('local_login', __name__)

# Funzione per controllare la validità della password
def controllaPassword(password):
    # Verifica se la password ha almeno 8 caratteri
    if len(password) < 8:
        flash("La password deve contenere almeno 8 caratteri.", "error")
        return False
    # Verifica se la password contiene almeno una lettera maiuscola
    if not re.search(r"[A-Z]", password):
        flash("La password deve contenere almeno una lettera maiuscola.", "error")
        return False
    # Verifica se la password contiene almeno una lettera minuscola
    if not re.search(r"[a-z]", password):
        flash("La password deve contenere almeno una lettera minuscola.", "error")
        return False
    # Verifica se la password contiene almeno un numero
    if not re.search(r"[0-9]", password):
        flash("La password deve contenere almeno un numero.", "error")
        return False
    # Verifica se la password contiene almeno un carattere speciale
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        flash("La password deve contenere almeno un carattere speciale.", "error")
        return False
    # Se tutte le condizioni sono soddisfatte, la password è valida
    return True

# Route per la pagina di login
@local_login_bp.route('/', methods=['GET', 'POST'])
def login_page():
    # Se il metodo della richiesta è POST, significa che l'utente sta cercando di effettuare il login
    if request.method == 'POST':
        # Recupera il nickname e la password inviati tramite il form
        username = request.form['nickname']
        password = request.form['password']

        # Recupera tutti gli utenti dal database
        utenti = db.get_Utente()
        # Cerca l'utente con il nickname fornito
        user_data = next((u for u in utenti if u[0] == username), None)
        
        # Se l'utente esiste
        if user_data:
            stored_nickname, stored_password = user_data
            # Verifica se la password fornita corrisponde a quella memorizzata
            if stored_password == password:
                # Se la password è corretta, effettua il login dell'utente
                user = User(nickname=stored_nickname)
                login_user(user)
                flash("Login effettuato!", "success")  # Messaggio di successo
                return redirect(url_for('home.homepage'))  # Reindirizza alla homepage
        
        # Se le credenziali non sono valide, mostra un messaggio di errore
        flash("Credenziali non valide.", "error")
        return redirect(url_for('local_login.login_page'))  # Ritorna alla pagina di login
    
    # Se la richiesta è GET, mostra la pagina di login
    return render_template('login.html')

# Route per la pagina di registrazione
@local_login_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    # Se il metodo della richiesta è POST, significa che l'utente sta cercando di registrarsi
    if request.method == 'POST':
        # Recupera il nickname e la password inviati tramite il form
        nickname = request.form['nickname']
        password = request.form['password']

        # Verifica che la password sia valida
        if not controllaPassword(password):
            return redirect(url_for('local_login.register_page'))  # Ritorna alla pagina di registrazione se la password non è valida

        # Recupera tutti gli utenti dal database
        utenti = db.get_Utente()
        # Controlla se il nickname è già stato preso
        if any(u[0] == nickname for u in utenti):
            flash('Nome utente già esistente!', 'error')  # Messaggio di errore
            return redirect(url_for('local_login.register_page'))  # Ritorna alla pagina di registrazione

        # Aggiungi il nuovo utente al database
        db.aggiungi_Utente(nickname, password)
        flash('Registrazione completata con successo!', 'success')  # Messaggio di successo
        return redirect(url_for('local_login.login_page'))  # Reindirizza alla pagina di login

    # Se la richiesta è GET, mostra la pagina di registrazione
    return render_template('register.html')
