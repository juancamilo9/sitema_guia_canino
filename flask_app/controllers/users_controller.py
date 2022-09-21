import json
from flask import Flask, render_template, request, redirect, session, jsonify
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
    return jsonify(message="correcto")


@app.route('/dashboard')
def dashboard():
    # validamos si no hay sesion inicada
    if 'user_id' not in session:
        return redirect('/')
    roles = Rol.get_all()
    print(f"Roles{roles}")
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
    if request.method == 'POST':
        errors = User.validate_user(request.form)
        if errors:
            return jsonify(errors)
        else:
            pwd = bcrypt.generate_password_hash(request.form['password'])
            form = {
                "first_name": request.form['first_name'],
                "last_name": request.form['last_name'],
                "number_phone": request.form['number_phone'],
                "email": request.form['email'],
                "address": request.form['address'],
                "password": pwd,
                "rol": request.form['rol']
            }
            User.save(form)
            return jsonify({'route': '/users'})
    return redirect('/users')


@app.route("/edit_user/<int:id>")
def edit_user(id):
    if 'user_id' not in session:
        return redirect('/')

    roles = Rol.get_all()
    form_user_edit = {
        "id": id
    }

    form = {
        "id": session['user_id']
    }
    user_to_edit = User.get_one(form_user_edit)
    print(user_to_edit.first_name)
    user = User.get_one(form)
    return render_template("users/edit.html", user=user, roles=roles, user_to_edit=user_to_edit)


@app.route("/update_user", methods=['POST'])
def update_user():
    if 'user_id' not in session:
        return redirect('/')
    errors = User.validate_update(request.form)
    if errors:
        return jsonify(errors)
    else:
        formulario = {
            "id": request.form['id'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "number_phone": request.form['number_phone'],
            "email": request.form['email'],
            "address": request.form['address'],
            "rol": request.form['rol']
        }
        User.update(formulario)
        return jsonify({'route':'/users'})



@app.route("/see_user/<int:id>")
def see_user(id):
    if 'user_id' not in session:
        return redirect('/')
    roles = Rol.get_all()
    form_user_edit = {
        "id": id
    }

    form = {
        "id": session['user_id']
    }
    user_to_edit = User.get_one(form_user_edit)
    print(user_to_edit.first_name)
    user = User.get_one(form)
    return render_template("users/see.html", user=user, roles=roles, user_to_edit=user_to_edit)


@app.route("/delete_user/<int:id>")
def delete_user(id):
    formulario = {
        "id": id
    }
    User.delete(formulario)
    return redirect('/users')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
