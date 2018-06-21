from application import db
from application.models import Base

from sqlalchemy.sql import text

class Comment(Base):
    text = db.Column(db.String(144), nullable=False)
    creator = db.Column(db.String(144), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)


    def __init__(self, text):
        self.text = text

    #return the amount of comments a thread has

    @staticmethod
    def threads_comments(thread_id):
        stmt = text("SELECT COUNT(*) FROM Comment WHERE Comment.thread_id = :thread_id").params(thread_id = thread_id)

        res = db.engine.execute(stmt)

        for row in res:
            return row[0]