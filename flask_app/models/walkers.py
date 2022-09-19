from flask_app.config.mysqlconnection import connectToMySQL


class Walker:
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.name_user = data['name_user']

    @classmethod
    def get_all(cls):
        query = "SELECT w.*, u.first_name as name_user FROM walkers AS w LEFT JOIN users AS u ON w.user_id = u.id WHERE u.rol_id = 2;"
        results = connectToMySQL('guia_canino').query_db(query)
        print(results)
        walkers = []
        for w in results:
            walkers.append(cls(w))
        return walkers

    @classmethod
    def save(cls, data):
        query = "INSERT INTO walkers(user_id) VALUES (%(user_id)s);"
        query1 = "UPDATE users SET rol_id=2 WHERE id = %(user_id)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        updated = connectToMySQL('guia_canino').query_db(query1, data)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM walkers WHERE id = %(id)s"
        result = connectToMySQL('guia_canino').query_db(query, data)
        query1 = "UPDATE users SET rol_id=3 WHERE id = %(user_id)s"
        updated = connectToMySQL('guia_canino').query_db(query1, data)
        return result


