from db.core import get_session
from db.transactions import get_transactions
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

router = APIRouter(
    prefix="/transactions",
)


@router.get("/")
async def get_all_transactions(request: Request, db: Session = Depends(get_session)):
    transactions = get_transactions(db)
    return transactions
