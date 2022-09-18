from flask_app.config.mysqlconnection import connectToMySQL
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_NUMBER_REGEX = re.compile(r'^[0-9]+$')
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

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, number_phone=%(number_phone)s, email=%(email)s, address=%(address)s, rol_id=%(rol)s WHERE id = %(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id=%(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        return result

    @staticmethod
    def validate_user(data):
        errors = {}
        if len(data['first_name']) < 3:
            errors['first_name'] = "Nombre debe tener 3 caracteres"

        if len(data['last_name']) < 3:
            errors['last_name'] = "Apellido debe tener 3 caracteres"

            # verificar formato correcto de email, expresiones regulares
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "E-mail invalido"

        if not PHONE_NUMBER_REGEX.match(data['number_phone']):
            errors['number_phone'] = "solo números para el telefono"

            # password con al menos 6 caracteres
        if len(data['password']) < 6:
            errors['password'] = "Contraseña debe tener al menos 6 caracteres"

            # password con al menos 6 caracteres
        if data['password'] != data['confirm_password']:
            errors['paasword1'] = "Contraseñas no coinciden"

            # consultar si ya existe el correo electronico en la base de datos
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('guia_canino').query_db(query, data)
        if len(results) >= 1:
            errors['email1'] = "E-mail registrado previamente"

        return errors

    @staticmethod
    def validate_update(data):

        errors = {}

        if len(data['first_name']) < 3:
            errors['first_name'] = "Nombre debe tener 3 caracteres"

        if len(data['last_name']) < 3:
            errors['last_name'] = "Apellido debe tener 3 caracteres"
            # verificar formato correcto de email, expresiones regulares

        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "E-mail invalido"

        if not PHONE_NUMBER_REGEX.match(data['number_phone']):
            errors['number_phone'] = "solo números para el telefono"
            # password con al menos 6 caracteres
        query = "SELECT * FROM users WHERE email = %(email)s and id != %(id)s;"
        result = connectToMySQL('guia_canino').query_db(query, data)
        print(result)
        if result:
            errors['email'] = "Email registrado previamente"
        return errors
