from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_mail import Mail
from flask_avatars import Avatars

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
socket = SocketIO(app)
mail = Mail(app)
avatars = Avatars(app)

login.login_view = 'user_routes.login'

# Create Data Acess Object
from models.DAO import DAO

dao = DAO(app)


# Registering blueprints
from routes.user_view import user_view
from routes.book_view import book_view

app.register_blueprint(user_view)
app.register_blueprint(book_view)


