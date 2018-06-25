from application import db
from application.models import Base

class Shoe(Base):
    model = db.Column(db.String(144), nullable=False)
    brand = db.Column(db.String(144), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)

    collection_id = db.Column(db.Integer, db.ForeignKey('collection.id'), nullable=False)

    def __init__(self, model, brand, release_year):
        self.model = model
        self.brand = brand
        self.release_year = release_year