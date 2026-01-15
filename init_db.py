from db import Base, engine
from models import *

Base.metadata.create_all(bind=engine)
print("Toutes les tables ont été recréées")