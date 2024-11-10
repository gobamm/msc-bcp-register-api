import uuid

import httpx
from v2.services.error_code_from_db import MessageService
from v2.apis.register.db_model import REGISTER_LOGIN_CODE_TRANS, REGISTER_LOGIN_VERIFY
from v2.services.bcp_otp_service import call_otp_request, call_otp_verify
from v2.settings.configs import  RIGISTER_CHECK_REQUEST #AUTH_URL, OTP_URL,
from v2.apis.register.model import AuthResponse, RegisterResponse, RegisterRequest, VerifyRequest, ConfirmRequest
from typing import Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
import uuid


# Validation functions
def validate_empty_fields(data: dict, required_fields: set, message_service: MessageService) -> Optional[dict]:
    missing_or_empty_fields = {field for field in required_fields if not data.get(field)}
    if missing_or_empty_fields:
        status_code = '90002'
        status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
        message = f"Missing or empty required fields: {', '.join(missing_or_empty_fields)}"
        status_message = status_message_template.replace("{message}", message)
        return RegisterResponse(
            status_code = status_code, 
            status_message = status_message,
        )
    return None

def validate_thai_id_and_phone_number(thai_id: str, phone_number: str, message_service: MessageService) -> Optional[RegisterResponse]:
    if len(thai_id) != 13 or not thai_id.isdigit():
        status_code = '90002'
        status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
        message = f"Thai ID must be 13 digits"
        status_message = status_message_template.replace("{message}", message)
        return RegisterResponse(
            status_code = status_code,
            status_message = status_message
        )
    
    if len(phone_number) != 10 or not phone_number.isdigit():
        status_code = '90002'
        status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
        message = f"Phone Number must be 10 digits"
        status_message = status_message_template.replace("{message}", message)
        return RegisterResponse(
            status_code = status_code,
            status_message = status_message
        )
    
    return None

def validate_otp_code_and_ref_code(otp_code: str, ref_code: str, message_service: MessageService) -> Optional[RegisterResponse]:

    # ตรวจสอบความยาวของ otp_code (ตัวอย่าง: 6 ตัวเลข)
    if len(otp_code) != 6 or not otp_code.isdigit():
        status_code = '90002'
        status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
        message = f"OTP code must be 6 digits"
        status_message = status_message_template.replace("{message}", message)
        return RegisterResponse(
            status_code = status_code,
            status_message = status_message
        )
    
    # ตรวจสอบความยาวของ ref_code (ตัวอย่าง: 6 ตัวอักษร)
    if len(ref_code) != 6:
        status_code = '90002'
        status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
        message = f"Ref code must be 8 characters"
        status_message = status_message_template.replace("{message}", message)
        return RegisterResponse(
            status_code = status_code,
            status_message = status_message
        )

    return None


# Core functions
def register_request(request: RegisterRequest, message_service: MessageService, http_request: Request, db: Session) -> RegisterResponse:

    # ตรวจสอบว่ามีข้อมูลครบหรือไม่
    required_fields = set(request.dict().keys())
    validation_error = validate_empty_fields(request.dict(), required_fields, message_service)
    if validation_error:
        return validation_error
   
    # ตรวจสอบว่ามีข้อมูล thai_id และ phone_number กรอกถูกต้องหรือไม่  
    validation_result = validate_thai_id_and_phone_number(request.thai_id, request.phone_number, message_service)
    if validation_result:
        return validation_result
    
    # ใช้ db (SQLAlchemy Session) สำหรับการ query ฐานข้อมูล
    existing_entry = db.query(REGISTER_LOGIN_VERIFY).filter(
        REGISTER_LOGIN_VERIFY.MOBILE_PHONE == request.phone_number
    ).first()

    # ตรวจสอบข้อมูลที่ query ได้
    if existing_entry:
        if existing_entry.VERIFY_DATE + timedelta(minutes=existing_entry.RESET_TIME) < datetime.now():
            db.delete(existing_entry)
            existing_entry = None
        elif existing_entry.VERIFY_COUNT >= existing_entry.LIMIT_COUNT:
            status_code = "90005"
            extended_time = existing_entry.VERIFY_DATE + timedelta(minutes=existing_entry.RESET_TIME)
            remaining_seconds = int((extended_time - datetime.now()).total_seconds())

            custom_message = message_service.get_message_string_code("register-request-v2", status_code)
                
            return RegisterResponse(
                status_code=status_code,
                status_message=custom_message,
                data= {
                    "sec": remaining_seconds
                }
            )
    print(f'existing_entry {existing_entry}')
    print(f'RegisterResponse {RegisterResponse}')

    register_check_request_body = {
        "thai_id": request.thai_id,
        "phone_number": request.phone_number
    }
    
    try:
        # ทำการเรียก API ตรวจสอบการลงทะเบียน
        response = httpx.post(f"{RIGISTER_CHECK_REQUEST}/api/member/v2/register-checkRequest", json=register_check_request_body)
        response_data = response.json()
        print(f"response_data11 {response_data}")
    except Exception as e:
        return RegisterResponse(
            status_code="50000",
            status_message=f"Failed to call register-checkRequest API: {e}"
        )
    
    if response_data.get("code") != "00000":
        # อัปเดตข้อมูลในฐานข้อมูลหากไม่สำเร็จ
        print(f'existing_entry {existing_entry}')
        if existing_entry:
            existing_entry.VERIFY_DATE = datetime.now()
            existing_entry.VERIFY_COUNT += 1
        else:
            new_entry = REGISTER_LOGIN_VERIFY(
                REGISTER_LOGIN_VERIFY_ID=str(uuid.uuid4()),
                MOBILE_PHONE=request.phone_number,
                VERIFY_TYPE='R',
                CHANNEL_CODE=request.channel_code,
                VERIFY_DATE=datetime.now(),
                LIMIT_COUNT=8,
                CREATED_DATE=datetime.now(),
                RESET_TIME=60,
                VERIFY_COUNT=1
            )
            db.add(new_entry)
        db.commit()

        status_code = response_data.get("code")
        status_message = response_data.get("message")

        return RegisterResponse(
            status_code=status_code,
            status_message=status_message
        )
    
    # เรียกใช้งาน API สำหรับ OTP Request โดยใช้ http_request สำหรับดึง headers
    otp_response = call_otp_request(request.phone_number, request.channel_code, message_service, http_request)
    if otp_response.status_code != "00000":
        return otp_response

    status_code = '00000'
    status_message = message_service.get_message_string_code("register-request-v2", status_code)
    
    return RegisterResponse(
        status_code=status_code, 
        status_message=status_message,
        data=otp_response.data
    )

    
    
def register_verify(request: VerifyRequest, db: Session, message_service: MessageService, http_request: Request) -> RegisterResponse:

    # ตรวจสอบว่ามีข้อมูลครบหรือไม่
    required_fields = set(request.dict().keys())
    validation_error = validate_empty_fields(request.dict(), required_fields, message_service)
    if validation_error:
        return validation_error
   
    # ตรวจสอบว่ามีข้อมูล thai_id และ phone_number กรอกถูกต้องหรือไม่  
    validation_result = validate_thai_id_and_phone_number(request.thai_id, request.phone_number, message_service)
    if validation_result:
        return validation_result
    
    # ตรวจสอบว่ามีข้อมูล ref_code และ otp_code กรอกถูกต้องหรือไม่    
    validation_responses = validate_otp_code_and_ref_code(request.otp_code, request.ref_code, message_service)
    if validation_responses:
        return validation_responses
    
    # เรียกใช้งาน API สำหรับ OTP Verify
    otp_response = call_otp_verify(request, message_service, http_request)
    print(otp_response)
    if otp_response.status_code != "00000":
        return otp_response
    
    # สร้าง register_login_code และบันทึกข้อมูล
    register_login_code = str(uuid.uuid4())  

    new_login_entry = REGISTER_LOGIN_CODE_TRANS(
        register_login_code=register_login_code,
        action_type='R', 
        phone_number=request.phone_number,
        # dob=datetime.strptime('31/10/2000', '%d/%m/%Y').date(),  
        verified_flag='N', 
        created_date=datetime.now(),
        updated_date=datetime.now(),  
    )
        
    db.add(new_login_entry)
    db.commit()
    
    status_code = '00000'
    status_message = message_service.get_message_string_code("register-request-v2", status_code)
    return RegisterResponse(
        status_code = status_code, 
        status_message = status_message,
        data={
            "register_code": register_login_code
        }
    )
    
def register_confirm(request: ConfirmRequest, db: Session, message_service: MessageService) -> RegisterResponse:
    # ตรวจสอบว่ามีข้อมูลครบหรือไม่
    required_fields = set(request.dict().keys())
    validation_error = validate_empty_fields(request.dict(), required_fields, message_service)
    if validation_error:
        return validation_error
    
    # ตรวจสอบว่ามีข้อมูล thai_id และ phone_number กรอกถูกต้องหรือไม่  
    validation_result = validate_thai_id_and_phone_number(request.thai_id, request.phone_number, message_service)
    if validation_result:
        return validation_result
    
    register_entry = db.query(REGISTER_LOGIN_CODE_TRANS).filter(
        REGISTER_LOGIN_CODE_TRANS.register_login_code == request.register_code,
        REGISTER_LOGIN_CODE_TRANS.action_type == 'R'
    ).first()

    if register_entry.verified_flag == 'Y':
        status_code = '90005'
        status_message = message_service.get_message_string_code("register-confirm-v2", status_code)
        return RegisterResponse(
            status_code = status_code,
            status_message = status_message
           )
    
    if register_entry.phone_number != request.phone_number or register_entry.register_login_code != request.register_code:
        status_code = '90003'
        status_message = message_service.get_message_string_code("register-confirm-v2", status_code)
        return RegisterResponse(
            status_code = status_code, 
            status_message = status_message,
    )
    
    register_entry.verified_flag = 'Y'
    register_entry.updated_date=datetime.now()
    db.commit()

    status_code = '00000'
    status_message = message_service.get_message_string_code("register-confirm-v2", status_code)
    return RegisterResponse(
        status_code = status_code, 
        status_message = status_message,
        data={
            "member_card": "00017890928"
        }
    )