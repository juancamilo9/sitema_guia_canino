from flask_app.config.mysqlconnection import connectToMySQL


class Rol:

    def __init__(self, data):
        self.id = data['id']
        self.rol = data['rol']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # consultar todos los tipos de roles
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM roles;"
        results = connectToMySQL('guia_canino').query_db(query)  # Lista de diccionarios
        roles = []
        # convierto cada una de las instacncias de la consulta en un objeto de la clase Rol
        for rol in results:
            roles.append(cls(rol))

        return roles

    @classmethod
    def save(cls, data):
        query = "INSERT INTO roles (rol) VALUES (%(rol)s);"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def update(cls, data):
        query = "UPDATE roles SET rol=%(rol)s WHERE id = %(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM roles WHERE id = %(id)s;"
        results = connectToMySQL('guia_canino').query_db(query, data)  # Lista de diccionarios
        return cls(results[0])

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM roles WHERE id=%(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate_rol(data):
        errors = {}
        if len(data['rol']) < 3:
            errors['rol'] = "El nombre del rol debe tener al menos tres caracteres"
        return errors
