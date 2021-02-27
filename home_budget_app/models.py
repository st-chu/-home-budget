from home_budget_app import db
from datetime import datetime

user_budget = db.Table('user_budget',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                       db.Column('budget_id', db.Integer, db.ForeignKey('budget.id'), primary_key=True)
                       )

locations = db.Table('locations',
                     db.Column('income_id', db.Integer, db.ForeignKey('income.id'), primary_key=True),
                     db.Column('deposit_id', db.Integer, db.ForeignKey('deposit.id'), primary_key=True)
                     )

saving_payment = db.Table('saving_payment',
                          db.Column('saving_id', db.Integer, db.ForeignKey('saving.id'), primary_key=True),
                          db.Column('payment_id', db.Integer, db.ForeignKey('payment.id'), primary_key=True)
                          )

debt_payment = db.Table('debt_payment',
                        db.Column('debt_id', db.Integer, db.ForeignKey('debt.id'), primary_key=True),
                        db.Column('payment_id', db.Integer, db.ForeignKey("payment.id"), primary_key=True)
                        )

expense_payment = db.Table('expense_payment',
                           db.Column('expense_id', db.Integer, db.ForeignKey('expense.id'), primary_key=True),
                           db.Column('payment_id', db.Integer, db.ForeignKey("payment.id"), primary_key=True)
                           )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User<'{self.username}', '{self.email}'>"


class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    posting_date = db.Column(db.String(10), nullable=False)
    steady_income = db.Column(db.Boolean, nullable=False, default=False)
    deposits = db.relationship('Deposit', secondary=locations, backref='incomes', lazy='subquery')

    def __repr__(self):
        return f"Income<'{self.name}', '{self.amount}zł', '{self.steady_income}'>"


class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(7), index=True, nullable=False)
    users = db.relationship('User', secondary=user_budget, backref='budgets', lazy='subquery')
    expenses = db.relationship('Expense', backref='budget', lazy=True)
    incomes = db.relationship('Income', backref='budget', lazy=True)
    savings = db.relationship('Saving', backref='budget', lazy=True)
    debts = db.relationship('Debt', backref='budget', lazy=True)

    def __repr__(self):
        return f"Budget<'{self.date}'>"


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    date_of_payment = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    steady_expense = db.Column(db.Boolean, nullable=False, default=False)
    payments = db.relationship('Payment', secondary=expense_payment, backref='expenses', lazy='subquery')

    def __repr__(self):
        return f"Expense<'{self.name}', '{self.amount}'zł, '{self.date_of_payment}', '{self.steady_expense}'>"


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    expenses = db.relationship('Expense', backref='category', lazy=True)

    def __repr__(self):
        return f"Category<'{self.name}'>"


class Deposit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    expenses = db.relationship('Expense', backref='deposit', lazy=True)
    savings = db.relationship('Saving', backref='deposit', lazy=True)
    debts = db.relationship('Debt', backref='deposit', lazy=True)

    def __repr__(self):
        return f"Deposit<'{self.name}', '{self.amount}'>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(250))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"Payment<'{self.amount}', '{self.date}', '{self.description}'>"


class Saving(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payments = db.relationship('Payment', secondary=saving_payment, backref='savings', lazy='subquery')

    def __repr__(self):
        return f"Saving<'{self.name}', '{self.amount}'>"


class Debt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'), nullable=False)
    deposit_id = db.Column(db.Integer, db.ForeignKey('deposit.id'), nullable=False)
    name = db.Column(db.String(100), index=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_of_payment = db.Column(db.String(10), nullable=False)
    payments = db.relationship('Payment', secondary=debt_payment, backref='debts', lazy='subquery')

    def __repr__(self):
        return f"Debt<'{self.name}', '{self.amount}', '{self.date_of_payment}'>"
