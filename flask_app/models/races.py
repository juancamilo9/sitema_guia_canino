from flask_app.config.mysqlconnection import connectToMySQL


class Race:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.danger = data['danger']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM races;"
        results = connectToMySQL('guia_canino').query_db(query)
        races = []
        for race in results:
            races.append(cls(race))
        return races

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM races WHERE id = %(id)s;"
        result = connectToMySQL('guia_canino').query_db(query,data)
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO races(name,danger) VALUES (%(name)s, %(danger)s);"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE races SET name = %(name)s, danger = %(danger)s WHERE id = %(id)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM races WHERE id = %(id)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate_race(data):
        errors = {}
        if len(data['name']) < 3:
            errors['name'] = "El nombre de la raza debe tener al menos tres caracteres"

        if data['danger'] == '':
            errors['danger'] = "El campo de peligro no debe ir vacio"

        return errors