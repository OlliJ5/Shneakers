from application import db
from application.models import Base

class Collection(Base):
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)


    def __init__(self, name):
        self.name = name