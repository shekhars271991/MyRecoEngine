from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

engine = create_engine('sqlite:///movies.db', echo=True)
Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=engine))

# Initialize the database
def init_db():
    Base.metadata.create_all(bind=engine)
