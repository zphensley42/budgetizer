from .. import db
from flask import Flask, render_template, redirect, url_for
from . import main

from ..models import Budget

@main.route("/")
def hello():
    return redirect(url_for('.showBudgets'), code=302)

@main.route("/budgets")
def showBudgets():

    # Get our budgets from the db
    budgetList = Budget.query.all()
    return render_template('budgets.html', budgets=budgetList)


@main.route('/budgets/<int:budget_id>')
def showBudget(budget_id):

    # Show the budget with the given id, the id is an integer
    budget = Budget.query.filter_by(id=budget_id).first()
    if budget is None:
        return render_template('errors/resource_not_found.html')
    else:
        return render_template('budget.html', budget=budget)
