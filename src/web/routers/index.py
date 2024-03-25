from fastapi import APIRouter
from starlette.responses import HTMLResponse, Response

from web.file_response import get_html_file_data

router = APIRouter()


@router.get("/")
async def index():
    return HTMLResponse(content=get_html_file_data("login.html"))


@router.get("/favicon.ico")
async def favicon():
    with open("web/static/images/favicon.ico", "rb") as f:
        return Response(content=f.read(), media_type="image/png")
