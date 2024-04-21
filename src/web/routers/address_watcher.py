from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse

from web.file_response import get_html_file_data

router = APIRouter()


@router.get("/address/{address}")
async def watch_address(request: Request):
    return HTMLResponse(content=get_html_file_data("address.html"))
