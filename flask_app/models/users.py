from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import jsonify


class User:

    # Metodo inicializador
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.number_phone = data['number_phone']
        self.email = data['email']
        self.address = data['address']
        self.is_admin = data['is_admin']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rol_id = data['rol_id']

    # Metodo para consultar en la bd por medio del correo
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        if len(result) < 1:
            return False
        else:
            user = cls(result[0])
            return user

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, number_phone, email, address, password, rol_id) VALUES (%(first_name)s, %(last_name)s, %(number_phone)s, %(email)s, %(address)s, %(password)s, %(rol)s);"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        if len(result) < 1:
            return False
        else:
            user = cls(result[0])
            return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('guia_canino').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users
