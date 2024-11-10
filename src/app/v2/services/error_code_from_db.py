from sqlalchemy.orm import Session
from v2.services.db_model import MSG_PARAMS, MSG_API_RESPONSE

class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def get_message_int_code(self, category: str, code: int) -> str:
        msg_param = self.db.query(MSG_PARAMS).filter(
            MSG_PARAMS.MSG_CATEGORY == category,
            MSG_PARAMS.MSG_CODE == code
        ).first()
        
        if msg_param:
            return msg_param.MSG_VALUE
        else:
            return "Message not found"

    def get_message_string_code(self, category: str, code: str) -> str:
        msg_param = self.db.query(MSG_API_RESPONSE).filter(
            MSG_API_RESPONSE.MSG_CATEGORY == category,
            MSG_API_RESPONSE.MSG_CODE == code
        ).first()
        
        if msg_param:
            return msg_param.MSG_VALUE
        else:
            return "Message not found"
