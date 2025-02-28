import ipdb
from sqlmodel import Session

from api.db.core import get_session, Transaction
from sqlmodel import select

db: Session = next(get_session())

print("FastAPI Shell - Database Session Loaded!")
ipdb.set_trace()
