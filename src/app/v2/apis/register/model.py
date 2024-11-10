from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class RegisterRequest(BaseModel):
    thai_id: str
    phone_number: str
    channel_code : str

class VerifyRequest(BaseModel):
    ref_code: str
    otp_code: str
    thai_id: str
    phone_number: str
    channel_code : str

class ConfirmRequest(BaseModel):
    register_code: str
    thai_id: str
    phone_number: str
    first_name_th: str
    last_name_th: str
    first_name_en: str
    last_name_en: str
    dob: str
    is_accept_consent1: bool
    is_accept_consent2: bool
    is_accept_consent3: bool
    friend_give_friend_flag: Optional[bool] = None
    channel_code: Optional[str] = None
    campaign_code: Optional[str] = None
    campaign_name: Optional[str] = None
    campaign_start: Optional[str] = None
    campaign_expired: Optional[str] = None
    campaign_detail: Optional[str] = None
    referral_member_id: Optional[str] = None
    referral_member_card_no: Optional[str] = None
    referral_first_name_th: Optional[str] = None
    referral_last_name_th: Optional[str] = None
    referral_first_name_en: Optional[str] = None
    referral_last_name_en: Optional[str] = None
    referral_mobile_no: Optional[str] = None

class AuthResponse(BaseModel):
    status_code: str
    status_message: str

class RegisterResponse(BaseModel):
    status_code: str
    status_message: str
    data: Optional[Dict[str, Any]] = Field(default=None)

