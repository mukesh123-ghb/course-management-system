from app.database import Base, engine
from app.models import *

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database reset: all tables dropped and recreated.")
