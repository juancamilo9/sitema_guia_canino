from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.races import Race
from flask_app.models.users import User
from flask_app import app
import json


@app.route('/races')
def races():
    if 'user_id' not in session:
        return redirect('/')
    races = Race.get_all()
    user = User.get_one({'id': session['user_id']})
    return render_template('races/index.html', races=races, user=user)


@app.route('/new_race')
def new_race():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    return render_template('races/new.html', user=user)


@app.route('/register_race', methods=['POST'])
def register_race():
    if request.method == 'POST':
        errors = Race.validate_race(request.form)
        if errors:
            return jsonify(errors)
        else:
            Race.save(request.form)
            return jsonify({'route': '/races'})
    return redirect('/races')


@app.route('/see_race/<int:id>')
def see_race(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    race = Race.get_by_id({'id': id})
    return render_template('races/see.html', user=user, race=race)


@app.route('/edit_race/<int:id>')
def edit_race(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    race = Race.get_by_id({'id': id})
    return render_template('races/edit.html', user=user, race=race)


@app.route('/update_race', methods=['POST'])
def update_race():
    if 'user_id' not in session:
        return redirect('/')
    errors = Race.validate_race(request.form)
    if errors:
        return jsonify(errors)
    else:
        Race.update(request.form)
        return jsonify({'route': '/races'})


@app.route('/delete_race/<int:id>')
def elete_rol(id):
    Race.delete({'id':id})
    return redirect('/races')


