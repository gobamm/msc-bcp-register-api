from sqlalchemy import Column, String, DateTime, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class REGISTER_LOGIN_CODE_TRANS(Base):
    __tablename__ = 'REGISTER_LOGIN_CODE_TRANS'

    register_login_code = Column(String(36), primary_key=True, nullable=False)
    action_type = Column(String(1), nullable=False)
    phone_number = Column(String(10), nullable=False)
    dob = Column(Date, nullable=False)
    verified_flag = Column(String(1), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, nullable=False)


class REGISTER_LOGIN_VERIFY(Base):
    __tablename__ = 'REGISTER_LOGIN_VERIFY'

    REGISTER_LOGIN_VERIFY_ID = Column(String(36), primary_key=True)
    MOBILE_PHONE = Column(String(20), nullable=False)
    VERIFY_TYPE = Column(String(3), nullable=False)
    CHANNEL_CODE = Column(String(20), nullable=False)
    LIMIT_COUNT = Column(Integer)
    CREATED_DATE = Column(DateTime)
    VERIFY_DATE = Column(DateTime)
    RESET_TIME = Column(Integer)
    VERIFY_COUNT = Column(Integer)
