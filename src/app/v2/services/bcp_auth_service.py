import httpx
from requests import Session
from v2.services.db_connection import get_db
from v2.services.error_code_from_db import MessageService
from v2.settings.configs import AUTH_URL
from v2.apis.register.model import AuthResponse
from fastapi import Depends, Header

# Call API BCP Auth Service
def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    return MessageService(db)

def call_bcp_auth_service(
        bcp_client_id: str = Header(None, alias="bcp_client_id"),
        bcp_client_secret: str = Header(None, alias="bcp_client_secret"),
        message_service: MessageService = Depends(get_message_service)
) -> AuthResponse:
    headers = {
        "bcp_client_id": bcp_client_id,
        "bcp_client_secret": bcp_client_secret
    }
    try:
        response = httpx.post(AUTH_URL + "/api/v2/client-verify", json=headers)
        response_data = response.json()
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        
        # Debugging information
        print(response_data)       
        if response_data.get("status_code") != 200:
            status_code = "90001"
            message = response_data.get("status_message")
            code = response_data.get("status_code")
            status_message_template = message_service.get_message_string_code("register-request-v2", status_code)            
            status_message = status_message_template.replace("{message}", message).replace("{code}", str(code))
            
            return AuthResponse(
                status_code=status_code,
                status_message=status_message
            )
        
        return AuthResponse(
            status_code="00000",
            status_message="Success",
        )
    
    except Exception as e:
        # Handle exceptions
        return AuthResponse(
            status_code="50000",
            status_message=f"General error: {e}"
        )
