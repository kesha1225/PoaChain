from fastapi import APIRouter

router = APIRouter()


@router.get("/is_alive")
async def is_alive():
    return {"alive": True}
