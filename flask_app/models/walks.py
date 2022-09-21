from flask_app.config.mysqlconnection import connectToMySQL


class Walk:
    def __init__(self, data):
        self.id = data['id']
        self.date_start = data['date_start']
        self.date_end = data['date_end']
        self.walker_id = data['walker_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.walker_name = data['walker_name']

    @classmethod
    def get_all(cls):
        query = 'SELECT w.*, u.first_name as walker_name FROM walks as w INNER JOIN walkers as wa ON w.walker_id = wa.id INNER JOIN users as u ON wa.user_id = u.id;'
        result = connectToMySQL('guia_canino').query_db(query)
        walks = []
        for w in result:
            walks.append(cls(w))
        return walks

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT w.*, u.first_name as walker_name FROM walks as w INNER JOIN walkers as wa ON w.walker_id = wa.id INNER JOIN users as u ON wa.user_id = u.id WHERE w.id = %(id)s;'
        result = connectToMySQL('guia_canino').query_db(query, data)
        print(result)
        return cls(result[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO walks (date_start, date_end, walker_id) VALUES (%(date_start)s, %(date_end)s, %(walker_id)s);"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE walks SET date_start=%(date_start)s, date_end=%(date_end)s, walker_id=%(walker_id)s WHERE id = %(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM walks WHERE id=%(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate_walk(data):
        errors = {}
        if data['date_start'] == '':
            errors['date_start'] = 'La fecha de inicio no puede ir en blanco'
        if data['date_end'] == '':
            errors['date_end'] = 'La fecha final no puede ir en blanco'
        if data['date_end'] < data['date_start']:
            errors['date_end'] = 'La fecha final no puede ser menor a la fecha de inicio'

        return errors




