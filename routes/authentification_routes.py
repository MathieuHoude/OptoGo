from flask import render_template, request, redirect, url_for, session, Blueprint
import os
import mysql.connector
from mysql.connector import Error
import bcrypt

from DB.utils import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# route pour la page d'authentification
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """This function handles the login process for the application.
It checks if the request method is POST, then retrieves the email and password from the request form.
It then queries the database for the user with the provided email.
If the user is found, it checks if the provided password matches the stored hashed password.
If the passwords match, it logs the user in and redirects to the index page.
If the passwords do not match, it sets an error message in the session and redirects back to the login page.
If the request method is not POST, it checks if a user is already logged in.
If a user is already logged in, it redirects to the index page.
If no user is logged in, it renders the login page template."""

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM optometristes WHERE email = "{email}"')
        optometriste = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if(optometriste is None):
            session["login_error"] = {'title': 'Erreur authentification', 'text': 'Veuillez vérifier votre email ou mot de passe'}
            return redirect(url_for("auth.login"))
        
        # Check if the provided password matches the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), optometriste['password'].encode()):
            session.pop('login_error', None)
            session["user"] = optometriste
            return redirect(url_for("index"))
        else:
            session["login_error"] = {'title': 'Erreur authentification', 'text': 'Veuillez vérifier votre email ou mot de passe'}
            return redirect(url_for("auth.login"))
    else :
        if 'user' in session:
            return redirect(url_for("index"))
        else:
            return render_template("loginPage.html")

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("auth.login"))