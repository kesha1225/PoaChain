from fastapi import APIRouter
from starlette.requests import Request

from crypto.sign import sign_message
from web.encryption import decrypt_text

router = APIRouter()


@router.post("/sign")
async def sign_handler(request: Request):
    return {
        "result": sign_message(
            message=(await request.json())["message"],
            private_key=decrypt_text(request.cookies["privateKey"]),
        )
    }
