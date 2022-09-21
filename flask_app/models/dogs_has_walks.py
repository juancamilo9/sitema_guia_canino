from flask_app.config.mysqlconnection import connectToMySQL


class DogWalk:

    def __init__(self, data):
        self.dog_id = data['dog_id']
        self.walk_id = data['walk_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.dog_name = data['dog_name']

        self.date_walk = data['date_walk']

    @classmethod
    def get_all(cls):
        query = "select dw.*, d.name as dog_name, w.date_start as date_walk from dogs_has_walks as dw inner join dogs d on d.id=dw.dog_id inner join walks w on w.id = dw.walk_id;"
        results = connectToMySQL('guia_canino').query_db(query)
        dogWalk = []
        for d in results:
            dogWalk.append(cls(d))
        return dogWalk

    @classmethod
    def get_by_id_walk(cls, data):
        query = "select dw.*, d.name as dog_name, w.date_start as date_walk  from dogs_has_walks as dw inner join dogs d on d.id=dw.dog_id inner join walks w on w.id = dw.walk_id where dw.walk_id=%(id)s;"
        results = connectToMySQL('guia_canino').query_db(query, data)
        dogWalk = []
        for d in results:
            dogWalk.append(cls(d))
        return dogWalk

    @classmethod
    def save(cls, data):
        query = "INSERT INTO dogs_has_walks(dog_id,walk_id) VALUES (%(dog_id)s, %(walk_id)s);"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM dogs_has_walks WHERE dog_id=%(dog_id)s AND walk_id=%(walk_id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate(data):
        errors = {}
        if data['walk_id'] == '':
            errors['walk_id'] = 'El campo caminata no debe ir vacio'
        if data['dog_id'] == '':
            errors['dog_id'] = 'El campo mascota no debe ir vacio'
        return errors



