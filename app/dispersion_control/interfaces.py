from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCView, ABCService

from app.archtool_conf.custom_layers import RoutersInitializationStrategyABC
from lib.db import init_db


class DispersionControlViewABC(ABCView):
    """
    апи упраления микросервиса, интегрируется с dispersion
    """

    @abstractmethod
    async def recreate_tables(self) -> None:
        """
        пересоздаёт таблицы бд
        """
        ...

    # TODO: нужны метрики, сколько уходит на injection
    #       какие зависимости
    # TODO: управление миграциями
    # TODO: выключение и включение микросервиса


class DispersionRoutesInitializerABC(RoutersInitializationStrategyABC):
    @abstractmethod
    def __call__(self):
        ...
