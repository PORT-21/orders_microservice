from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCView, ABCService

from lib.db import init_db
from .interfaces import DispersionControlViewABC


class DispersionControlView(DispersionControlViewABC):

    async def recreate_tables(self) -> None:
        init_db(drop_db=True)
