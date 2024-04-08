from fastapi import APIRouter

from web.file_response import get_html_file_data

router = APIRouter()


@router.get("/is_alive")
async def is_alive():
    return {"alive": True}
