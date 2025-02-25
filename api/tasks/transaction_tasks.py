import pandas as pd

from api.db.core import get_session
from api.db.transactions import (check_and_create_transactions,
                                 get_existing_date_list)
from api.utils.load import get_transaction_details
from api.worker.celery import app


@app.task
def task_create_transaction(df_json: str):
    df = pd.read_json(df_json)

    with next(get_session()) as db:
        existing_date_list = get_existing_date_list(db)
        transactions = get_transaction_details(df, existing_date_list)
        print("Transactions extracted successfully")

        if transactions:
            print("Updating the DB with the transactions")
            check_and_create_transactions(transactions, db)
            print("task_create_transaction successufull")
