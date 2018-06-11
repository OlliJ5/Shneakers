from application import db
from application.models import Base

class Comment(Base):
    text = db.Column(db.String(144), nullable=False)
    creator = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)


    def __init__(self, text):
        self.text = text