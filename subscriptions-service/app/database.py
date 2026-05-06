# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv
# import os

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")

# engine = None
# SessionLocal = None


# def init_db():
#     global engine, SessionLocal

#     import os
#     from dotenv import load_dotenv
#     from sqlalchemy import create_engine
#     from sqlalchemy.orm import sessionmaker

#     load_dotenv()

#     db_url = os.getenv("DATABASE_URL")

#     if not db_url:
#         raise Exception("DATABASE_URL is not set")

#     engine = create_engine(db_url, echo=True)
#     SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("DATABASE_URL is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)