from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.races import Race
from flask_app.models.users import User
from flask_app.models.dogs import Dog
from flask_app import app
import json


@app.route('/dogs')
def dogs():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    dogs = Dog.get_all()
    return render_template('dogs/index.html', dogs=dogs, user=user)


@app.route('/new_dog')
def register_dogs():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    races = Race.get_all()
    owners = User.get_all()
    return render_template('dogs/new.html', races=races, owners=owners, user=user)


@app.route('/register_dog', methods=['POST'])
def register_dog():
    if request.method == 'POST':
        errors = Dog.validate_dog(request.form)
        if errors:
            return jsonify(errors)
        else:
            age = int(request.form['age'])
            form = {
                'name': request.form['name'],
                'age': age,
                'color': request.form['color'],
                'owner_id': request.form['owner_id'],
                'race_id': request.form['race_id'],
            }
            Dog.save(form)
            return jsonify({'route': '/dogs'})
    return redirect('/dogs')


@app.route('/see_dog/<int:id>')
def see_dog(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    dog = Dog.get_by_id({'id': id})
    return render_template('dogs/see.html', user=user, dog=dog)


@app.route('/edit_dog/<int:id>')
def edit_dog(id):
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    dog = Dog.get_by_id({'id': id})
    owners = User.get_all()
    races = Race.get_all()
    return render_template('dogs/edit.html', user=user, dog=dog, owners=owners, races=races)


@app.route('/update_dog', methods=['POST'])
def update_dog():
    if 'user_id' not in session:
        return redirect('/')
    errors = Dog.validate_dog(request.form)
    print(errors)
    if errors:
        return jsonify(errors)
    else:
        age = int(request.form['age'])
        form = {
            'id': request.form['id'],
            'name': request.form['name'],
            'age': age,
            'color': request.form['color'],
            'owner_id': request.form['owner_id'],
            'race_id': request.form['race_id']
        }
        Dog.update(form)
        return jsonify({'route': '/dogs'})


@app.route('/delete_dog/<int:id>')
def delete_dog(id):
    Dog.delete({'id': id})
    return redirect('/dogs')
