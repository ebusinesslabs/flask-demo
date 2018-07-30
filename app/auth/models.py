from datetime import datetime
from .. import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(256))
    roles = db.Column(db.String(1024))
    status = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow())


    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        print "User<{}, {}>".format(self.username, self.email)