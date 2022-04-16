#===================================================={ all imports }============================================================

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#==================================================={ global objects }==========================================================

USER = os.getenv("POSTGRES_USER")
PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
HOST = os.getenv("POSTGRES_URL")

# comment the below lines to use sqlite for testing
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    DATABASE_URL = f"postgresql://{USER}:{PASS}@{HOST}/{DB_NAME}"
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

engine = create_engine(DATABASE_URL)

# uncomment the below lines to use sqlite database for testing
# DATABASE_URL = 'sqlite:///database.db'
# engine = create_engine(DATABASE_URL, connect_args={'check_same_thread':False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#==================================================={ get_db function }=========================================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#====================================================={ Code ends here }========================================================
