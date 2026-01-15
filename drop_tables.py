from db import Base, engine

# Supprime toutes les tables
Base.metadata.drop_all(bind=engine)
print("Toutes les tables ont été supprimées")
