from datetime import datetime
from typing import Annotated, List

from fastapi import Depends
from pydantic import BaseModel
from sqlmodel import Session, func, select

from api.db.core import Transaction, get_session
from api.utils import datetime_utils


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


def create_transaction_obj(
    transaction_date: str,
    description: str,
    type_of_transaction: str,
    amount: float,
    payment_method: str,
    transaction_id: str,
    payee: str,
    category: str,
):
    return Transaction(
        transaction_date=transaction_date,
        description=description,
        type_of_transaction=type_of_transaction,
        amount=amount,
        payment_method=payment_method,
        payee=payee,
        category=category,
        transaction_id=transaction_id,
    )


def create_transactions(transactions: List, session: Session) -> None:
    session.add_all(transactions)
    session.commit()


def get_existing_date_list(session: Session) -> list:
    existing_dates = session.exec(select(Transaction.transaction_date).distinct())
    existing_dates_list = list(existing_dates)

    return existing_dates_list


def check_and_create_transactions(transactions: List[Transaction], session: Session):
    existing_dates_list = get_existing_date_list(session)
    existing_datetime_list = list(
        map(datetime_utils.convert_datetime_str_to_datetime, existing_dates_list)
    )
    print("Existing date list ", existing_datetime_list)

    new_data = [
        transaction
        for transaction in transactions
        if transaction.transaction_date not in existing_datetime_list
    ]
    length_of_data = len(new_data)

    print("New data", new_data)

    if new_data:
        create_transactions(new_data, session)
        print(f"Number of new transactions created: {length_of_data}")

    return len(new_data)
