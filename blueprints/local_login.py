from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user
import re  # Import necessario per controllaPassword

local_login_bp = Blueprint('local_login', __name__)

def controllaPassword(password):
    if len(password) < 8:
        flash("La password deve contenere almeno 8 caratteri.", "error")
        return False
    if not re.search(r"[A-Z]", password):
        flash("La password deve contenere almeno una lettera maiuscola.", "error")
        return False
    if not re.search(r"[a-z]", password):
        flash("La password deve contenere almeno una lettera minuscola.", "error")
        return False
    if not re.search(r"[0-9]", password):
        flash("La password deve contenere almeno un numero.", "error")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        flash("La password deve contenere almeno un carattere speciale.", "error")
        return False
    return True

@local_login_bp.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['nickname']
        password = request.form['password']

        utenti = db.get_Utente()
        user_data = next((u for u in utenti if u[0] == username), None)
        
        if user_data:
            stored_nickname, stored_password = user_data
            if stored_password == password:
                user = User(nickname=stored_nickname)
                login_user(user)
                flash("Login effettuato!", "success")
                return redirect(url_for('home.homepage'))
        
        flash("Credenziali non valide.", "error")
        return redirect(url_for('local_login.login_page'))
    
    return render_template('login.html')

@local_login_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        if not controllaPassword(password):
            return redirect(url_for('local_login.register_page'))

        utenti = db.get_Utente()
        if any(u[0] == nickname for u in utenti):
            flash('Nome utente già esistente!', 'error')
            return redirect(url_for('local_login.register_page'))

        db.aggiungi_Utente(nickname, password)
        flash('Registrazione completata con successo!', 'success')
        return redirect(url_for('local_login.login_page'))

    return render_template('register.html')