from . import db

# Models
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40))
    amount = db.Column(db.Integer)

    def __init__(self, title, amount):
        self.title = title
        self.amount = amount

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'title': self.title,
           'amount': self.amount
       }
