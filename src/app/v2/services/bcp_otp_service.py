from fastapi import Request
import httpx
from v2.services.error_code_from_db import MessageService
from v2.settings.configs import OTP_URL
from v2.apis.register.model import AuthResponse, RegisterResponse, VerifyRequest

# #call api otp service
def call_otp_request(phone_number: str, channel_code: str, message_service: MessageService, http_request: Request) -> RegisterResponse:

    try:
        otp_request_body = {
            "mobile_no": phone_number,
            "channel_code": channel_code    
        }
        headers = {
            'bcp_client_id': http_request.headers.get('bcp_client_id'),
            'bcp_client_secret': http_request.headers.get('bcp_client_secret'),
            'Content-Type': 'application/json'
        }
        try:

            response = httpx.post(OTP_URL+"/api/v2/otp-request",headers = headers, json = otp_request_body)
            response_data = response.json()
            print(f"response_data22 {response_data}")
        except Exception as e:
            return RegisterResponse(
                status_code="50000",
                status_message=f"Failed to call OTP API: {e}"
            )
        if response_data.get("status_code") != 200:
            if response_data.get("status_code") == 907:
                status_code = "90004"
                message = response_data.get("status_message")
                code = response_data.get("status_code")
                status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
                status_message = status_message_template.replace("{message}", message).replace("{code}", str(code))
                remaining_sec = response_data.get("data", {}).get("sec", 0)
                return RegisterResponse(
                    status_code=status_code,
                    status_message=status_message,
                    data= {
                        "sec" : remaining_sec
                    }
                )
            else: 
                status_code = "90003"
                message = response_data.get("status_message")
                code = response_data.get("status_code")
                status_message_template = message_service.get_message_string_code("register-request-v2", status_code)
                status_message = status_message_template.replace("{message}", message).replace("{code}", str(code))

                return RegisterResponse(
                    status_code=status_code,
                    status_message=status_message
            )
        
        ref_code = response_data["data"]["ref_code"]

        return RegisterResponse(
            status_code="00000",
            status_message="Success",
            data={
                "ref_code": ref_code,
            }
        )
    except Exception as e:
        return RegisterResponse(
            status_code="50000",
            status_message="general error",
        )

def call_otp_verify(request: VerifyRequest, message_service: MessageService, http_request: Request) -> RegisterResponse:
    try:
        otp_verify_body = {
            "ref_code": request.ref_code,
            "otp_code": request.otp_code,
            "mobile_no": request.phone_number,
            "channel_code": request.channel_code  
        }
        headers = {
            'bcp_client_id': http_request.headers.get('bcp_client_id'),
            'bcp_client_secret': http_request.headers.get('bcp_client_secret'),
            'Content-Type': 'application/json'
        }

        try:
            otp_response = httpx.post(OTP_URL + "/api/v2/otp-verify",headers = headers, json = otp_verify_body)
            otp_response_data = otp_response.json()

        except Exception as e:
            return RegisterResponse(
                status_code="50000",
                status_message=f"Failed to call OTP Verify API: {e}"
            )
    
        if otp_response_data.get("status_code") != 200:
            if otp_response_data.get("status_code") == 906:
                status_code = "90004"
                message = otp_response_data.get("status_message")
                code = otp_response_data.get("status_code")
                status_message_template = message_service.get_message_string_code("register-verify-v2", status_code)
                status_message = status_message_template.replace("{message}", message).replace("{code}", str(code))
                remaining_sec = otp_response_data.get("data", {}).get("sec", 0)
                return RegisterResponse(
                    status_code=status_code,
                    status_message=status_message,
                    data= {
                        "sec" : remaining_sec
                    }
                ) 
            else:   
                status_code = "90003"
                message = otp_response_data.get("status_message")
                code = otp_response_data.get("status_code")
                status_message_template = message_service.get_message_string_code("register-verify-v2", status_code)
                status_message = status_message_template.replace("{message}", message).replace("{code}", str(code))

                return RegisterResponse(
                    status_code=status_code,
                    status_message=status_message
                )
    
        return RegisterResponse(
            status_code="00000",
            status_message="OTP verified successfully",
        )
    except Exception as e:
        return RegisterResponse(
            status_code="50000",
            status_message="general error",
        )