from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.roles import Rol
from flask_app.models.users import User
from flask_app import app
import json


@app.route('/roles')
def roles():
    if 'user_id' not in session:
        return redirect('/')
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    roles = Rol.get_all()
    return render_template('roles/index.html', roles=roles, user=user)


@app.route('/new_rol')
def new_rol():
    if 'user_id' not in session:
        return redirect('/')
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    return render_template('roles/new.html', user=user)


@app.route('/register_rol', methods=['POST'])
def register_rol():
    if 'user_id' not in session:
        return redirect('/')
    if request.method == 'POST':
        errors = Rol.validate_rol(request.form)
        if errors:
            return jsonify(errors)
        else:
            Rol.save(request.form)
            return jsonify({'route': '/roles'})
    return redirect('/roles')


@app.route('/see_rol/<int:id>')
def see_rol(id):
    if 'user_id' not in session:
        return redirect('/')
    rol = Rol.get_by_id({'id':id})
    form = {
        "id": session['user_id']
    }
    user = User.get_one(form)
    return render_template("roles/see.html", user=user, rol=rol)


@app.route('/edit_rol/<int:id>')
def edit_rol(id):
    if 'user_id' not in session:
        return redirect('/')
    # get information of bd
    rol = Rol.get_by_id({'id':id})
    user = User.get_one({'id':session['user_id']})
    return render_template('roles/edit.html', rol=rol, user=user)


@app.route('/update_rol', methods=['POST'])
def update_rol():
    if 'user_id' not in session:
        return redirect('/')
    errors = Rol.validate_rol(request.form)
    if errors:
        return jsonify(errors)
    else:
        Rol.update(request.form)
        return jsonify({'route': '/roles'})


@app.route('/delete_rol/<int:id>')
def delete_rol(id):
    Rol.delete({'id':id})
    return redirect('/roles')

