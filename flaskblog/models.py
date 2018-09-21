from flaskblog import db, login_manager
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from flask_login import UserMixin


# we import login_manager here cause it will handle all of the sessions in
# background. The extension has to know how to find one of your users by ID.

# This sets the callback for reloading a user from the session. The
#         function you set should take a user ID (a ``unicode``) and return a
#         user object, or ``None`` if the user does not exist.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# image_file --> String 20 characters cause we will transit it to a hash value
# and so do the password, we save a 60 hash value in db.
# the instance you have created will autimatically set the table name.
# It’s derived from the class name converted to lowercase and with “CamelCase” converted to “camel_case”.
# To override the table name, set the __tablename__ class attribute.
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # the user model are actually referencing the post class, so we use uppercase 'P'
    # the posts attribute is not actually a column itself.That is actually running an
    # additional query on the post table the grabs any post from that user.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # Magic method, it specify how it print when we print the object out.
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    # the foreign key referencing the table name and the column name,so it's use lower case.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
