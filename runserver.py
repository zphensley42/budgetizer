from app import create_app, db
from app.models import Budget

app = create_app()

@app.cli.command('seedBudgets')
def seedBudgets():
    """Seed the db with budgets"""

    db.create_all()

    budget1 = Budget("Budget 1", 5000)
    budget2 = Budget("Budget 2", 7000)
    budget3 = Budget("Budget 3", 2000)
    budget4 = Budget("Budget 4", 1500)

    db.session.add(budget1)
    db.session.add(budget2)
    db.session.add(budget3)
    db.session.add(budget4)
    db.session.commit()

    print("Seeded the database with budgets")

    budgetList = Budget.query.all()
    print(budgetList)


if __name__ == '__main__':

    print('printing known routes: ')
    print(app.url_map)
    app.run()
