from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

from chain.db import Base
from chain_config import PostgresConfig

engine = create_async_engine(PostgresConfig.db_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


def db_session(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if "session" in kwargs:
            return await func(*args, **kwargs)

        async with async_session() as session:
            result = await func(session, *args, **kwargs)
        return result

    return wrapper
