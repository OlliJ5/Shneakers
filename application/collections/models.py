from application import db
from application.models import Base

class Collection(Base):
    name = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(144))

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    shoes = db.relationship("Shoe", backref='collection', lazy=True)

    def __init__(self, name):
        self.name = name