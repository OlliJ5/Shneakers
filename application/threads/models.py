from application import db
from application.models import Base

from sqlalchemy.sql import text

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

    #return the top 5 most commented threads

    @staticmethod
    def most_commented_threads():
        stmt = text("SELECT Thread.id, Thread.date_created, Thread.date_modified,"
                    " Thread.title, Thread.text, Thread.creator, Thread.category_name,"
                    " Thread.account_id, Thread.category_id, COUNT(Comment.id)"
                    " FROM Thread LEFT JOIN Comment on Comment.thread_id = thread.id"
                    " GROUP BY Thread.id order by COUNT(comment.id) DESC LIMIT 5")

        res = db.engine.execute(stmt)

        response = []

        for row in res:
            response.append({"id": row[0],
                            "date_created": row[1],
                            "date_modified": row[2],
                            "title": row[3],
                            "text": row[4],
                            "creator": row[5],
                            "category_name": row[6],
                            "account_id": row[7],
                            "category_id": row[8],
                            "comments": row[9]})  

        for row in response:
            print(row)

        return response      
