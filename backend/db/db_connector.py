import os
from sqlalchemy import create_engine

from db.models import Base


def get_db_url():
    db_url = ""
    try:
        db_url = os.getenv("DATABASE_URL", default=None)
        if db_url is None:
            raise EnvironmentError("DB URL not set in environment variables")
    except EnvironmentError as e:
        print(f"An error occurred while getting the database URL: {str(e)}")
    except Exception as e:
        print(f"An error occurred while getting the database URL: {str(e)}")
    finally:
        return db_url


# Create the database engine
DATABASE_URL = get_db_url()
engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

# Create all tables in the database
# This will create tables if they don't exist
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)