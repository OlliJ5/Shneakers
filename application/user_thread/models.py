from application import db
from application.models import Base

from sqlalchemy.sql import text

class UserThread(Base):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable = False)

    def __init__(self, thread_id):
        self.thread_id = thread_id

    @staticmethod
    def how_many_viewers_a_thread_has(thread_id):
        stmt = text("SELECT COUNT(*) FROM user_thread"
                    " WHERE thread_id = :thread_id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        for row in res:
            return row[0]

    @staticmethod
    def how_many_unique_viewers_a_thread_has(thread_id):
        stmt = text("SELECT COUNT(distinct account_id) FROM user_thread"
                    " WHERE thread_id = :thread_id").params(thread_id=thread_id)

        res = db.engine.execute(stmt)

        for row in res:
            return row[0]