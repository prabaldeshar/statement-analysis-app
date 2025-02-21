from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///expenses.db"


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_date: str
    description: str
    type_of_transaction: str
    amount: float
    payment_method: str
    payee: str
    category: str
    transaction_id: str


connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
