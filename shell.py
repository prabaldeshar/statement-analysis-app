import os
import sys

import ipdb
from sqlmodel import Session, func, select

from api.db.core import Transaction, get_session
from api.main import app

db: Session = next(get_session())

print("FastAPI Shell - Database Session Loaded!")
ipdb.set_trace()
