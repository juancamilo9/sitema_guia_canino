import json
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_app.models.walkers import Walker
from flask_app import app
from flask_app.models.walks import Walk
from flask_app.models.users import User
from flask_app.models.dogs import Dog
from flask_app.models.dogs_has_walks import DogWalk


@app.route('/walks')
def walks():
    if 'user_id' not in session:
        return redirect('/')
    walks = Walk.get_all()
    user = User.get_one({'id': session['user_id']})
    dog_walk = DogWalk.get_all()
    return render_template('walks/index.html', walks=walks, user=user, dog_walk=dog_walk)


@app.route('/new_walk')
def new_walk():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    walkers = Walker.get_all()
    walks = Walk.get_all()
    print(walkers)
    return render_template('walks/new.html', user=user, walkers=walkers, walks=walks)


@app.route('/register_walk', methods=['POST'])
def register_walk():
    if request.method == 'POST':
        errors = Walk.validate_walk(request.form)
        if errors:
            return jsonify(errors)
        else:
            Walk.save(request.form)
            return jsonify({'route': '/walks'})
    return redirect('/walks')


@app.route("/see_walk/<int:id>")
def see_walk(id):
    if 'user_id' not in session:
        return redirect('/')
    walk = Walk.get_by_id({'id': id})
    dog_walk = DogWalk.get_by_id_walk({'id': id})
    print(dog_walk)
    user = User.get_one({"id": session['user_id']})
    return render_template("walks/see.html", user=user, walk=walk, dog_walk=dog_walk)


@app.route('/edit_walk/<int:id>')
def edit_walk(id):
    if 'user_id' not in session:
        return redirect('/')
    walkers = Walker.get_all()
    walk = Walk.get_by_id({'id': id})
    user = User.get_one({"id": session['user_id']})
    return render_template("walks/edit.html", user=user, walk=walk, walkers=walkers)


@app.route("/update_walk", methods=['POST'])
def update_walk():
    if 'user_id' not in session:
        return redirect('/')
    errors = Walk.validate_walk(request.form)
    if errors:
        return jsonify(errors)
    else:
        Walk.update(request.form)
        return jsonify({'route': '/walks'})


@app.route('/delete_walk/<int:id>')
def delete_walk(id):
    Walk.delete({'id': id})
    return redirect('/walks')


@app.route('/new_dog_walk')
def new_dog_walker():
    if 'user_id' not in session:
        return redirect('/')
    user = User.get_one({'id': session['user_id']})
    dogs = Dog.get_all()
    walks = Walk.get_all()
    return render_template('walks/new_dog_walk.html', dogs=dogs, walks=walks, user=user)


@app.route('/register_dog_walk', methods=['POST'])
def register_dog_walk():
    if request.method == 'POST':
        errors = DogWalk.validate(request.form)
        if errors:
            return jsonify(errors)
        else:
            DogWalk.save(request.form)
            return jsonify({'route': '/walks'})
    return redirect('/walks')


@app.route('/delete_dog_walk/<int:dog_id>/<int:walk_id>')
def delete_dog_walk(dog_id, walk_id):
    DogWalk.delete(
        {'dog_id': dog_id,
         'walk_id': walk_id
         })
    return redirect('/walks')
