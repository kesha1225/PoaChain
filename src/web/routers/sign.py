from fastapi import APIRouter
from starlette.requests import Request

from crypto.sign import sign_message
from web.encryption import decrypt_text

router = APIRouter()


@router.post("/sign")
async def sign_handler(request: Request):
    request_data = await request.json()

    return {
        "result": sign_message(
            message=request_data["message"],
            private_key=decrypt_text(request_data["private_key"]),
        )
    }
