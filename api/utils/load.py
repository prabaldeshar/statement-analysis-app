from datetime import datetime

import plotly.express as px
from api.services.infer import infer
from models import (create_transaction_obj, create_transactions,
                    get_all_transactions, get_transactions_grouped_by_category)
from api.utils.process_excel import process_raw_excel

file_path = "data/statement-2025-01-01-to-2025-01-01.xlsx"


def insert_transation(file_path):
    df = process_raw_excel(file_path)

    all_transactions = []
    for index, row in df.iterrows():
        datetime_str = row["TRANSACTION DATE"]
        description = row["DESCRIPTION"]
        withdraw = row["WITHDRAW"]
        deposit = row["DEPOSIT"]
        amount = 0

        dt_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        date_only = dt_obj.date()

        if withdraw != "-":
            type_of_transaction = "withdraw"
            amount = float(withdraw.replace(",", ""))
        else:
            type_of_transaction = "deposit"
            amount = float(deposit.replace(",", ""))

        response = infer(description)
        response["type_of_transaction"] = type_of_transaction
        response["date"] = date_only

        payment_method = response.get("transfer", {}).get("transfer_type", "QR")
        payee = response.get("transfer", {}).get("destination", "self")

        transaction = create_transaction_obj(
            date=dt_obj,
            description=description,
            type_of_transaction=type_of_transaction,
            amount=amount,
            payment_method=payment_method,
            payee=payee,
            category=response["category"],
            transaction_id=response["transaction_id"],
        )
        all_transactions.append(transaction)

    print("Creating all transactions....")
    create_transactions(all_transactions)


def get_transactions():
    all_transactions = get_all_transactions()
    return all_transactions


def main():
    # all_transactions = get_transactions()
    transaction_by_category = get_transactions_grouped_by_category()
    labels = []
    values = []
    for transaction in transaction_by_category:
        labels.append(transaction[0])
        values.append(transaction[1])

    fig = px.pie(names=labels, values=values)
    fig.show()


if __name__ == "__main__":
    main()
