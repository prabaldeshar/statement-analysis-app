from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile
from sqlmodel import Session

from api.db.core import get_session
from api.tasks.transaction_tasks import task_create_transaction
from api.utils.process_excel import process_raw_excel

router = APIRouter(
    prefix="/upload",
)


@router.post("/statement/")
async def upload_statement(file: UploadFile, db: Session = Depends(get_session)) -> dict:
    """
        Upload bank statement
    """
    contents = await file.read()
    buffer = BytesIO(contents)

    df = process_raw_excel(buffer)
    df_json = df.to_json(orient="records")

    task = task_create_transaction.delay(df_json)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully, processing the file",
        "task_id": task.id,
    }
