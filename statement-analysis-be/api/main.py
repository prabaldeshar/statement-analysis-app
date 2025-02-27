from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db.core import init_db
from api.routers.expenses import router as expenses_router
from api.routers.filter import router as filter_router
from api.routers.tasks import router as tasks_router
from api.routers.transactions import router as transaction_router
from api.routers.upload import router as upload_router

test_router = APIRouter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@test_router.get("/posts")
async def posts():
    return {"posts": "test"}


app.include_router(transaction_router)
app.include_router(expenses_router)
app.include_router(filter_router)
app.include_router(upload_router)
app.include_router(tasks_router)
app.include_router(test_router)


@app.get("/")
def read_root():
    return "Server is running."
