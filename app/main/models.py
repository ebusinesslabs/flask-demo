from .. import db


class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    entity = db.Column(db.String(128), unique=True)
    value = db.Column(db.String(256))

    def __init(self, entity, value = ''):
        self.entity = entity
        self.value = value

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Config: {}, {}>'.format(self.entity, self.value)
