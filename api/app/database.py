import os
from  dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
#establishes a connection to the postgres container
engine = create_engine(DATABASE_URL)
#creates the session factory which just makes sessions
Session_Local = sessionmaker(engine)

def get_db():
    #creates an actual session
    db = Session_Local()
    try:
        yield db    #hands session to the API endpoint
    finally:
        db.close()  #closes the session when the endpoint is done