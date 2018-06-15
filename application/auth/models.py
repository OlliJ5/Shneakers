from application import db
from application.models import Base
#from application.threads.models import association_table

from sqlalchemy.sql import text

class User(Base):

    __tablename__ = "account"

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    createdThreads = db.relationship("Thread", backref='account', lazy=True)
    comments = db.relationship("Comment", backref='account', lazy=True)

    #threads = db.relationship("Thread", secondary=association_table, back_populates="accounts")

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def find_how_many_tasks_each_user_has():
        stmt = text("SELECT Account.id, Account.username, COUNT(Thread.id) FROM Account"
                    " LEFT JOIN Thread ON Thread.account_id = Account.id"
                    " GROUP BY Account.id")

        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "username":row[1], "posts":row[2]})

        return response