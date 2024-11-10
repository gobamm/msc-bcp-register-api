from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class MSG_PARAMS(Base):
    __tablename__ = 'MSG_PARAMS'
    
    MSG_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    MSG_CATEGORY = Column(String(255), nullable=False)
    MSG_CODE = Column(Integer, nullable=False)
    MSG_VALUE = Column(String(4000), nullable=False)

class MSG_API_RESPONSE(Base):
    __tablename__ = 'MSG_API_RESPONSE'

    MSG_ID = Column(BigInteger, primary_key=True, autoincrement=True)
    MSG_CATEGORY = Column(String(255), nullable=False)
    MSG_CODE = Column(String(10), nullable=False)
    MSG_VALUE = Column(String(4000), nullable=False)
    
