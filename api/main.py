from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.expenses import router as expenses_router
from routers.filter import router as filter_router
from routers.transactions import router as transaction_router

test_router = APIRouter()


app = FastAPI()
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
app.include_router(test_router)


@app.get("/")
def read_root():
    return "Server is running."
