from app import create_app, db
from app.models import Budget, Transaction, Category, CategoriesTransactions
from datetime import datetime

app = create_app()

@app.cli.command('seedDb')
def seedDb():
    """Seed the db"""

    db.create_all()

    # Budgets
    budget1 = Budget("Budget 1", 5000)
    db.session.add(budget1)

    # Categories
    category1 = Category("Category 1", 200.00)
    category2 = Category("Category 2", 800.00)
    db.session.add(category1)
    db.session.add(category2)

    # Budget-Category links
    budget1.categories.append(category1)
    budget1.categories.append(category2)


    # Transactions
    transaction1 = Transaction("Business 1", "Outflow transaction", datetime.now())
    transaction2 = Transaction("Business 2", "Inflow transaction", datetime.now())
    transaction3 = Transaction("Business 3", "Split transaction", datetime.now())
    db.session.add(transaction1)
    db.session.add(transaction2)
    db.session.add(transaction3)

    # CategoriesTransactions links (many-to-many)
    link1 = CategoriesTransactions(outflow=25.00)
    link1.category = category1
    link1.transaction = transaction1

    link2 = CategoriesTransactions(inflow=10.00)
    link2.category = category2
    link2.transaction = transaction2

    link3 = CategoriesTransactions(outflow=50.00)
    link3.category = category1
    link3.transaction = transaction3

    link4 = CategoriesTransactions(outflow=50.00)
    link4.category = category2
    link4.transaction = transaction3


    category1.transactions.append(link1)
    category2.transactions.append(link2)
    category1.transactions.append(link3)
    category2.transactions.append(link4)

    db.session.commit()

    print("Seeded the database")

    budgetList = Budget.query.all()
    print(budgetList)


if __name__ == '__main__':

    print('printing known routes: ')
    print(app.url_map)
    app.run()
