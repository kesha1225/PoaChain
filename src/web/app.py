from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import index_router, mnemonic_router, wallet_router


app = FastAPI()
app.include_router(index_router)
app.include_router(mnemonic_router)
app.include_router(wallet_router)
app.mount("/css", StaticFiles(directory="web/static/css/"), name="css")
app.mount("/html", StaticFiles(directory="web/static/html/"), name="html")
app.mount("/js", StaticFiles(directory="web/static/js/"), name="js")
app.mount("/images", StaticFiles(directory="web/static/images/"), name="images")


# todo: валидация блока и транзы
# todo: написать что все зашифровано в куках
