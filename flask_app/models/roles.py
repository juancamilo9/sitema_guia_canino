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