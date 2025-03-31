from datetime import datetime, timezone, tzinfo
from enum import Enum
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


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime


class Dated(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


def get_enum_values(e: Enum) -> list:
    return [val.value for key, val in e.__members__.items()]

import sqlalchemy as sa
from archtool.utils import string_to_snake_case


def create_enum_column(enum: Enum) -> sa.Enum:
    enum_col_T = sa.Enum(*get_enum_values(enum), name=string_to_snake_case(enum.__name__), metadata=Base.metadata, create_constraint=True, validate_strings=True)
    return enum_col_T
