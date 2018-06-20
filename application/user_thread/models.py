from application import db
from application.models import Base

class UserThread(Base):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable = False)

    def __init__(self, thread_id):
        self.thread_id = thread_id