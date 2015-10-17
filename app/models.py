from . import db

# triple quote = string literal that can span lines

# Models
class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    amount = db.Column(db.Integer)
    categories = db.relationship('Category', backref='budget', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    @property
    def serialize(self):
       print('Returning Budget object data in serializable format')
       return {
           'id': self.id,
           'title': self.title,
           'amount': self.amount,
           'categories': [i.serialize for i in self.categories]
       }


# Join table for many-to-many (Category & Transaction)
class CategoriesTransactions(db.Model):
    __tablename__ = 'categories_transactions'
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'), primary_key=True)
    inflow = db.Column(db.Float)
    outflow = db.Column(db.Float)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    amount = db.Column(db.Float)
    budgetId = db.Column(db.Integer, db.ForeignKey('budget.id'))
    transactions = db.relationship('CategoriesTransactions', backref='category')
    # backref adds .category to join table

    def __init__(self, title, amount):
        self.title = title
        self.amount = amount

    @property
    def serialize(self):
       print('Returning Category object data in serializable format')
       return {
           'title': self.title,
           'amount': self.amount,
           'budgetId': self.budgetId,
           'transactions': [i.transaction.serialize(i) for i in self.transactions]
       }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to = db.Column(db.String(128))
    notes = db.Column(db.String(256))
    createdAt = db.Column(db.Date)
    categories = db.relationship('CategoriesTransactions', backref='transaction')
    # backref adds .transaction to join table

    def __init__(self, to, notes, createdAt):
        self.to = to
        self.notes = notes
        self.createdAt = createdAt

    def serialize(self, assoc):
       print('Returning Transaction object data in serializable format')
       return {
           'id': self.id,
           'to': self.to,
           'notes': self.notes,
           'createdAt': self.createdAt,
           'outflow': 0 if assoc.outflow == None else assoc.outflow,
           'inflow': 0 if assoc.inflow == None else assoc.inflow
       }
