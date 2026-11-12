import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.connection import engine

from app.database.connection import engine
from app.database.base import Base

from app.models.user import User
from app.models.task import Task

Base.metadata.create_all(bind=engine)

print("Tables created!")