from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCView, ABCService
from fastapi import APIRouter

from app import config
from lib.db import init_db
from .interfaces import DispersionControlViewABC, DispersionRoutesInitializerABC


class DispersionRoutesInitializer(DispersionRoutesInitializerABC):
    router = APIRouter(prefix="/dispersion", tags=['dispersion'])
    dispersion_view: DispersionControlViewABC

    def __call__(self):
        self.router.add_api_route("/recreate_tables", self.dispersion_view.recreate_tables, methods=["POST"], operation_id="recreate_tables")

from lib.db import Base
from sqlalchemy.ext.asyncio import AsyncEngine


class DispersionControlView(DispersionControlViewABC):
    engine: AsyncEngine

    async def recreate_tables(self) -> None:
        await init_db(drop_db=True,
                db_uri=config.SQLALCHEMY_DATABASE_URI_ASYNC,
                Base=Base,
                engine=self.engine)
