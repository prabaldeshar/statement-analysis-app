from io import BytesIO

from fastapi import APIRouter, Depends, File, Request, UploadFile
from sqlmodel import Session

from api.db.core import get_session
from api.db.transactions import check_and_create_transactions, get_transactions
from api.utils.load import get_transactions
from api.utils.process_excel import process_raw_excel

router = APIRouter(
    prefix="/upload",
)


@router.post("/statement/")
async def upload_statement(file: UploadFile, db: Session = Depends(get_session)):
    contents = await file.read()
    buffer = BytesIO(contents)

    # TODO run part in the background
    transactions = get_transactions(buffer, db)
    print("Transactions extracted successfully")

    if transactions:
        print("Updating the DB with the transactions")
        check_and_create_transactions(transactions, db)

    return {"filename": file.filename, "message": "File uploaded successfully"}
