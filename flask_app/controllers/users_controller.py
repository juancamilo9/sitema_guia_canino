from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.users import User
from flask_app.models.roles import Rol
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
        return jsonify(message='E-mail no encontrado')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        return jsonify(message='Password incorrecto')

    session['user_id'] = user.id
    print(session['user_id'])
    return jsonify(message="correcto")


@app.route('/dashboard')
def dashboard():
    # validamos si no hay sesion inicada
    if 'user_id' not in session:
        return redirect('/')
    roles = Rol.get_all()
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    return render_template('dashboard.html', roles=roles, user=user)


@app.route('/users')
def users():
    if 'user_id' not in session:
        return redirect('/')
    roles = Rol.get_all()
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    users = User.get_all()
    return render_template('users/index.html', user=user, roles=roles, users=users)


@app.route('/new_user')
def new():
    if 'user_id' not in session:
        return redirect('/')
    roles = Rol.get_all()
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    return render_template('users/new.html', roles=roles, user=user)


@app.route('/register', methods=['POST'])
def register_user():
    pwd = bcrypt.generate_password_hash(request.form['password'])  # Encriptamos el password del usuario

    formulario = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "number_phone": request.form['number_phone'],
        "email": request.form['email'],
        "address": request.form['address'],
        "password": pwd,
        "rol": request.form['rol']

    }
    # Envio los datos al modelo para que sean procesados
    User.save(formulario)

    return redirect('/users')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
