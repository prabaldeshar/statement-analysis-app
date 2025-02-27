from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from api.db.core import get_session
from api.db.transactions import FilterField, get_filter_fields

router = APIRouter(
    prefix="/filter-fields",
)


@router.get("/")
async def get_filters(request: Request, db: Session = Depends(get_session)) -> FilterField:
    """
        Retrive the table fields(columns) which be used as filters in the Frontend table
    """
    filter_fields = get_filter_fields(db)
    return filter_fields
