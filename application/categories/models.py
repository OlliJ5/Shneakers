from application import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)

    threads = db.relationship("Thread", backref='category', lazy=True)

    def __init__(self, name):
        self.name = name