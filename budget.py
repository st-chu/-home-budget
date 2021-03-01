from home_budget_app import app, db
from home_budget_app.models import User, Budget, Income, Category, Deposit, Payment, Expense, Debt, Saving, add_new


@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Budget': Budget,
        'Income': Income,
        'Category': Category,
        'Deposit': Deposit,
        'Payment': Payment,
        'Expense': Expense,
        'Debt': Debt,
        'Saving': Saving,
        'add_new': add_new
    }
