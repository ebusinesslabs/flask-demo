from datetime import datetime
from .. import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

user_role = db.Table('user_role',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                     )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(256))
    status = db.Column(db.Boolean)
    image = db.Column(db.String(256))
    token = db.Column(db.String(64))
    # Note the lack of parenthesis after datetime.utcnow
    # You need to pass the callable itself not calling the function immediately
    created = db.Column(db.DateTime, default=datetime.utcnow)
    roles = db.relationship(
        'Role', secondary=user_role
    )
    # articles = db.relationship('Article', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def has_role(self, role):
        for r in self.roles:
            if role == r.name:
                return True
        return False

    def __repr__(self):
        return '<User: {}, {}, {}>'.format(self.username, self.email, self.fullname)

    def __str__(self):
        return self.username


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

    def __str__(self):
        return self.name

    def save(self):
        db.session.add(self)
        db.session.commit()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
