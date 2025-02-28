from celery.result import AsyncResult
from fastapi import APIRouter

from api.worker.celery import app

router = APIRouter(
    prefix="/tasks",
)


@router.get("/status/{task_id}")
async def get_task_status(task_id: str) -> dict:
    """
        Check the background task's status
    """
    task_result = AsyncResult(task_id, app=app)

    if task_result.status == "SUCCESS":
        return {"task_id": task_id, "status": "SUCCESS", "message": "Statement processed successfully"}
    elif task_result.status == "PENDING":
        return {"task_id": task_id, "status": "PENDING", "message": "Processing your statement..."}
    else:
        return {"task_id": task_id, "status": "FAILED", "message": "Processing failed, please try again"}
