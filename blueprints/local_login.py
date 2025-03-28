from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.models import DatabaseWrapper
import pymysql

# Creiamo l'oggetto database
db = DatabaseWrapper(host="localhost", user="root", password="password", database="SpotifyDB")

local_login_bp = Blueprint('local_login', __name__)

@local_login_bp.route('/')
def login_page():
    return render_template('login.html')

@local_login_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        nickname = request.form['nickname']
        password = request.form['password']

        # Controlliamo se l'utente esiste già
        utenti = db.get_Utente()
        if any(u['nickname'] == nickname for u in utenti):
            flash('Nome utente già esistente!', 'error')
            return redirect(url_for('local_login.register_page'))

        # Salviamo l'utente
        db.aggiungi_Utente(nickname, password)
        flash('Registrazione completata con successo!', 'success')
        return redirect(url_for('local_login.login_page'))

    return render_template('register.html')