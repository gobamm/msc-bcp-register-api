from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from v2.services.error_code_from_db import MessageService
from v2.services.db_connection import get_db
from v2.services.bcp_auth_service import call_bcp_auth_service
from v2.apis.register.model import RegisterRequest, RegisterResponse, VerifyRequest, ConfirmRequest, AuthResponse
from v2.apis.register.mainmod import register_request ,register_verify, register_confirm

router = APIRouter()

@router.post("/register-request", response_model=RegisterResponse, response_model_exclude_none=True)
async def register(
    request: RegisterRequest, 
    http_request: Request,  # สำหรับดึง headers จาก HTTP request
    db: Session = Depends(get_db),  # db ใช้สำหรับ query ข้อมูลจากฐานข้อมูล
    auth_response: AuthResponse = Depends(call_bcp_auth_service)
):
    # ตรวจสอบ auth_response ก่อน
    if auth_response.status_code != "00000":
        return AuthResponse(
            status_code=auth_response.status_code, 
            status_message=auth_response.status_message
        )
    
    message_service = MessageService(db)  # ใช้ db สำหรับสร้าง message_service
    
    # เรียกใช้งาน register_request โดยส่ง db และ http_request อย่างถูกต้อง
    return register_request(request, message_service, http_request, db)

@router.post("/register-verify", response_model=RegisterResponse, response_model_exclude_none=True)
async def verify(
    request: VerifyRequest,
    http_request: Request,
    db: Session = Depends(get_db),
    auth_response: AuthResponse = Depends(call_bcp_auth_service)
):    
    if auth_response.status_code != "00000":
        return AuthResponse(
            status_code=auth_response.status_code, 
            status_message=auth_response.status_message
        )
    message_service = MessageService(db)
    return register_verify(request, db, message_service, http_request)

@router.post("/register-confirm", response_model=RegisterResponse, response_model_exclude_none=True)
async def confirm(
    request: ConfirmRequest,
    db: Session = Depends(get_db),
    auth_response: AuthResponse = Depends(call_bcp_auth_service)
):    
    if auth_response.status_code != "00000":
        return AuthResponse(
            status_code=auth_response.status_code, 
            status_message=auth_response.status_message
        )
    message_service = MessageService(db)
    return register_confirm(request, db, message_service)


