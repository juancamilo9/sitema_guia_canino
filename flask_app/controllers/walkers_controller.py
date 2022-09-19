import json
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.walkers import Walker
from flask_app import app
from flask_app.models.users import User


@app.route('/walkers')
def walkers():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    walkers = Walker.get_all()
    return render_template('walkers/index.html', walkers=walkers, user=user)


@app.route('/new_walker')
def new_walker():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    users = User.get_all()
    return render_template('walkers/new.html', user=user, users=users)


@app.route('/register_walker', methods=['POST'])
def register_walker():
    if request.method == 'POST':
        Walker.save(request.form)
        return jsonify({'route': '/walkers'})


@app.route('/delete_walker/<int:id>/<int:user_id>')
def delete_walker(id, user_id):
    Walker.delete({'id': id, 'user_id': user_id})
    return redirect('/walkers')
