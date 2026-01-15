from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://postgres:@localhost/pycrypto')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)