from datetime import datetime, timezone, tzinfo
import typing as t

from furl import furl
from sqlalchemy import create_engine
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

from lib.dtos import Paginataion


Base = declarative_base()


def get_no_db_engine(dsn):
    f = furl(dsn)
    db_name = f.path.segments[0]
    f.path.remove(db_name)  # Remove database name from DSN
    return create_engine(f.url, isolation_level="AUTOCOMMIT")


def get_db_name(dsn: str) -> str:
    f = furl(dsn)
    return f.path.segments[0]



T = t.TypeVar("T")

def paginate(query: T, pag_info: Paginataion) -> T:
    offset = (pag_info.page - 1) * pag_info.size
    paginated = query.offset(offset).limit(pag_info.size)
    return paginated


def get_now(tz: tzinfo = timezone.utc) -> datetime:
    return datetime.now(tz=tz)



async def init_db(Base: DeclarativeMeta,
                  db_uri: str,
                  engine: AsyncEngine,
                  drop_db: bool):
    dbschema = "public"
    async with engine.begin() as conn:
        from sqlalchemy.sql import text
        if drop_db:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.execute(text(f'set search_path={dbschema}'))
            await conn.run_sync(Base.metadata.create_all)


async def drop_db(Base: DeclarativeMeta, db_uri: str) ->  AsyncEngine:    
    engine = create_async_engine(db_uri, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    return engine
