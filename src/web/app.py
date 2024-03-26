from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import index_router, mnemonic_router, wallet_router, sign_router


app = FastAPI()
app.include_router(index_router)
app.include_router(mnemonic_router)
app.include_router(wallet_router)
app.include_router(sign_router)
app.mount("/css", StaticFiles(directory="web/static/css/"), name="css")
app.mount("/html", StaticFiles(directory="web/static/html/"), name="html")
app.mount("/js", StaticFiles(directory="web/static/js/"), name="js")
app.mount("/images", StaticFiles(directory="web/static/images/"), name="images")


# надо:
# 0. нода для чейн отдельная вебапка
# 1. todo: get_wallet_data поменять чтобы он ходил в ноду а не в базу
# todo: чтобы нода как то по пруф оф авторити работала
# 2. todo: првоерять что кука протухла и разлогинивать!
# 3. todo: автообновление валлета типа что поменялся баланс


# прочее:
# todo: валидация блока и транзы
# todo: докер
# todo: поднять реально в вебе чтобы по куеру могли зайти

# отчет:
# todo: написать что все зашифровано в куках
# todo: описать что такое bech32 и почему именно он
# в базах юзаются индексы
