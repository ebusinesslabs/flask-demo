from .. import db
from datetime import datetime


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(256))
    body = db.Column(db.Text)
    image = db.Column(db.String(256))
    status = db.Column(db.Boolean)
    createdat = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Article: {}, {}>'.format(self.id, self.title)
