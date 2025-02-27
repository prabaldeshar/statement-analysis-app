from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from api.db.core import get_session
from api.db.transactions import get_transactions

router = APIRouter(
    prefix="/transactions",
)


@router.get("/")
async def get_all_transactions(request: Request, db: Session = Depends(get_session)):
    """
        Get all transactions
    """
    transactions = get_transactions(db)
    return transactions
