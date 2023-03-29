from flask_app.config.mysqlconnection import connectToMySQL
import re
AGE_REGEX = re.compile(r'^[0-9]+$')

class Dog:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.color = data['color']
        self.owner_id = data['owner_id']
        self.race_id = data['race_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.race_name = data['race_name']
        self.owner_name = data['owner_name']

    @classmethod
    def get_all(cls):
        query = 'SELECT d.*, r.name as race_name, o.first_name as owner_name FROM dogs as d INNER JOIN users as o ON d.owner_id = o.id INNER JOIN races as r ON d.race_id = r.id;'
        result = connectToMySQL('guia_canino').query_db(query)
        dogs = []
        for d in result:
            dogs.append(cls(d))
        return dogs
    

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT d.*, r.name as race_name, o.first_name as owner_name FROM dogs as d INNER JOIN users as o ON d.owner_id = o.id INNER JOIN races as r ON d.race_id = r.id WHERE d.id = %(id)s;'
        result = connectToMySQL('guia_canino').query_db(query, data)
        if len(result) < 1:
            return False
        else:
            dog = cls(result[0])
            return dog

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO dogs(name,age,color,owner_id,race_id) VALUES(%(name)s,%(age)s,%(color)s,%(owner_id)s, %(race_id)s);'
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM dogs WHERE id=%(id)s'
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = 'UPDATE dogs SET name=%(name)s,age=%(age)s,color=%(color)s,owner_id=%(owner_id)s,race_id=%(race_id)s WHERE id=%(id)s'
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate_dog(data):
        errors = {}
        if len(data['name']) < 3:
            errors['name'] = 'El nombre de la mascota debe tener al menmos tres caracteres'

        if data['age'] == "":
            errors['age'] = "La edad no puede ir vacia"

        if not AGE_REGEX.match(data['age']):
            errors['age1'] = "La edad del perro debe ser digitada en numeros"

        if data['color'] == "":
            errors['color'] = "El color de la mascota no debe ir vacio"
        print(errors)
        return errors




