from datetime import datetime
from typing import Annotated, List, Optional

from db.core import Transaction, get_session
from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, func, select


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ExpenseCategory(BaseModel):
    category: str
    amount: float


class PaymentMethodCategory(BaseModel):
    payment_method: str
    amount: float


class Expense(BaseModel):
    date: str
    amount: float


class FilterField(BaseModel):
    category: List[str]
    payment_methods: List[str]


class TransactionResponse(BaseModel):
    transaction_date: str
    description: str
    type_of_transaction: str
    amount: float
    payment_method: str
    payee: str
    category: str
    transaction_id: str


SessionDep = Annotated[Session, Depends(get_session)]


def get_expense_categories(session: SessionDep):
    statement = (
        select(Transaction.category, func.sum(Transaction.amount))
        .where(Transaction.type_of_transaction == "withdraw")
        .group_by(Transaction.category)
    )
    trasactions = session.exec(statement).all()
    expenses = [
        ExpenseCategory(category=transaction[0], amount=transaction[1])
        for transaction in trasactions
    ]
    return expenses


def get_expense_by_payment_method(session: SessionDep):
    statement = (
        select(Transaction.payment_method, func.sum(Transaction.amount))
        .where(Transaction.type_of_transaction == "withdraw")
        .group_by(Transaction.payment_method)
    )
    trasactions = session.exec(statement).all()

    expenses = [
        PaymentMethodCategory(payment_method=transaction[0], amount=transaction[1])
        for transaction in trasactions
    ]

    print(expenses)
    return expenses


def get_all_expenses_ordered_by_date(session: SessionDep):
    statement = (
        select(Transaction.transaction_date, func.sum(Transaction.amount))
        .where(Transaction.type_of_transaction == "withdraw")
        .group_by(Transaction.transaction_date)
        .order_by(Transaction.transaction_date)
    )
    transactions = session.exec(statement).all()

    expenses = [
        Expense(date=transaction[0], amount=transaction[1])
        for transaction in transactions
    ]
    return expenses


def get_filter_fields(session: SessionDep):
    statement = select(Transaction.category).distinct()
    categories = session.exec(statement).all()

    statement = select(Transaction.payment_method).distinct()
    payment_methods = session.exec(statement).all()

    return FilterField(
        category=[category for category in categories],
        payment_methods=[payment_method for payment_method in payment_methods],
    )


def get_transactions(session: SessionDep):
    statement = select(Transaction)
    transactions = session.exec(statement).all()

    # Convert transaction_date to date string
    formatted_transactions = [
        {
            **transaction.dict(),
            "transaction_date": datetime.strptime(
                transaction.transaction_date, "%Y-%m-%d %H:%M:%S"
            ).strftime("%Y-%m-%d"),
        }
        for transaction in transactions
    ]

    return formatted_transactions
