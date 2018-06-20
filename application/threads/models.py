from application import db
from application.models import Base


class Thread(Base):
    title = db.Column(db.String(144), nullable=False)
    text = db.Column(db.String(400), nullable=False)
    creator = db.Column(db.String(144), nullable=False)
    category_name = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    comments = db.relationship("Comment", backref='thread', lazy=True)

    thread_users = db.relationship("UserThread", backref='thread', lazy=True)

    def __init__(self, title, text):
        self.title = title
        self.text = text
