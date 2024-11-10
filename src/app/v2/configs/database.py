from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy.engine import URL
from v2.settings.configs import DATABASE_PASSWORD,DATABASE_USERNAME,DATABASE_HOST,DATABASE_SCHEMA

DATABASE_URL = URL.create(
    "mssql+pyodbc",
    username=DATABASE_USERNAME,
    password=DATABASE_PASSWORD,  
    host=DATABASE_HOST,
    database=DATABASE_SCHEMA,
    query={"driver": "ODBC Driver 17 for SQL Server"}
)
SQLALCHEMY_DATABASE_URL = DATABASE_URL 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,poolclass=QueuePool, pool_size=10, max_overflow=20
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)