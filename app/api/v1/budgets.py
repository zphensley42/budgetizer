from flask import jsonify, request, g, url_for, current_app
from ... import db
from ...models import Budget
from . import api_v1


@api_v1.route("/budgets", methods=['GET'])
def getBudgets():

    # Get budgets from the db
    budgetList = Budget.query.all()

    return jsonify(data=[i.serialize for i in budgetList])

@api_v1.route('/budgets/clear', methods=['POST'])
def clearBudgets():

    # Clear budgets from the db
    Budget.query.delete()
    db.session.commit()
    resp = {'message': 'Budgets successfully cleared'}
    return jsonify(resp)

@api_v1.route('/budgets/add', methods=['POST'])
def addBudget():

    # Get our budget data
    data = request.form
    if data:
        newBudget = Budget(data['title'], data['amount'])
        db.session.add(newBudget)
        db.session.commit()

        resp = {'message': 'Budget successfully added', 'budget': newBudget.serialize}
        return jsonify(resp)

    respData = {'message': 'Budget failed to be added'}
    resp = Response(json.dumps(respData), status=400, mimetype='application/json')  # 400: bad request
    return resp
