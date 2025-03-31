from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import DatabaseWrapper


# Creiamo l'oggetto database
db = DatabaseWrapper(db_file="SpotifyDB.db")

local_login_bp = Blueprint('local_login', __name__)

@local_login_bp.route('/')
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash("Login effettuato!", "success")
            return redirect(url_for('home.homepage'))
        flash("Credenziali non valide.", "error")
        return redirect(url_for('login'))

    return render_template('login.html')



@local_login_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        # Controlliamo se l'utente esiste già
        utenti = db.get_Utente()
        if any(u[1] == nickname for u in utenti):
            flash('Nome utente già esistente!', 'error')
            return redirect(url_for('local_login.register_page'))

        # Salviamo l'utente
        db.aggiungi_Utente(nickname, password)
        flash('Registrazione completata con successo!', 'success')
        return redirect(url_for('local_login.login_page'))

    return render_template('register.html')