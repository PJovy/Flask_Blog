import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


# Configurations of this Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '4bc1b881eaf412e6f5c47225e90db40c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in !'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.sina.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '15678911669@sina.cn'
app.config['MAIL_PASSWORD'] = 'PenG6118'
mail = Mail(app)



from flaskblog import routes

