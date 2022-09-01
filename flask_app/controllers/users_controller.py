from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.users import User
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)


# Ruta para inicio de sesion
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    # verificar que el email exista
    user = User.get_by_email(request.form)
    if not user:
        jsonify('E-mail no encontrado', 'login')
        return redirect('/')
    # bcrypt.check_password_hash(user.password, request.form['password'])
    if not user.password == request.form['password']:
        jsonify('Password incorrecto', 'login')
        return redirect('/')

    session['user_id'] = user.id

    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')