from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine
from api.config.settings import settings

DATABASE_URL = f"postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"


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


engine = create_engine(
    DATABASE_URL,
)


async def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
