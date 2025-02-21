from db.core import get_session
from db.transactions import (get_all_expenses_ordered_by_date,
                             get_expense_by_payment_method,
                             get_expense_categories)
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

router = APIRouter(
    prefix="/expenses",
)


@router.get("/")
async def get_all_expenses(request: Request, db: Session = Depends(get_session)):
    expenses = get_all_expenses_ordered_by_date(db)
    return expenses


@router.get("/category/")
async def get_expenses_by_category(reqest: Request, db: Session = Depends(get_session)):
    expenses = get_expense_categories(db)
    return expenses


@router.get("/payment-method/")
async def get_expenses_by_payment_method(
    request: Request, db: Session = Depends(get_session)
):
    expenses = get_expense_by_payment_method(db)
    return expenses
