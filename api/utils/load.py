from datetime import datetime
from typing import List

from fastapi import Depends
from sqlmodel import Session

from api.db.core import Transaction, get_session
from api.db.transactions import create_transaction_obj, get_existing_date_list
from api.services.openai_service import OpenAIService
from api.utils.process_excel import process_raw_excel


def determine_transaction_type(withdraw, deposit):
    if withdraw != "-":
        return "withdraw", float(withdraw.replace(",", ""))
    else:
        return "deposit", float(deposit.replace(",", ""))


def get_transactions(file_path, db) -> List[Transaction]:
    df = process_raw_excel(file_path)
    openai_service = OpenAIService()
    existing_date_list = get_existing_date_list(db)
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
