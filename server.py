from flask_app import app
from flask_app.controllers import races_controllers, dogs_controller, users_controller, walks_controller, walkers, roles_controller

if __name__ == "__main__":
    app.run(debug=True)
