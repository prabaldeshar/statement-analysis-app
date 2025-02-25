from datetime import datetime
from typing import List

from pandas import DataFrame

from api.db.core import Transaction
from api.db.transactions import create_transaction_obj
from api.services.openai_service import OpenAIService


def determine_transaction_type(withdraw, deposit):
    if withdraw != "-":
        return "withdraw", float(withdraw.replace(",", ""))
    else:
        return "deposit", float(deposit.replace(",", ""))


def get_transaction_details(
    df: DataFrame, existing_date_list: List
) -> List[Transaction]:
    openai_service = OpenAIService()
    all_transactions = []

    for index, row in df.iterrows():
        datetime_str = row["TRANSACTION DATE"]
        description = row["DESCRIPTION"]
        withdraw = row["WITHDRAW"]
        deposit = row["DEPOSIT"]
        amount = 0.0

        if datetime_str in existing_date_list:
            print(f"Skipping row {index}")
            continue

        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")

        date_only = dt_obj.date()

        type_of_transaction, amount = determine_transaction_type(withdraw, deposit)

        response = openai_service.infer(description)
        response["type_of_transaction"] = type_of_transaction
        response["date"] = date_only

        payment_method = response.get("transfer", {}).get("transfer_type", "QR")
        payee = response.get("transfer", {}).get("destination", "self")
        category = response["category"]
        transaction_id = response["transaction_id"]

        transaction = create_transaction_obj(
            transaction_date=dt_obj,
            description=description,
            type_of_transaction=type_of_transaction,
            amount=amount,
            payment_method=payment_method,
            payee=payee,
            category=category,
            transaction_id=transaction_id,
        )

        all_transactions.append(transaction)

    return all_transactions
