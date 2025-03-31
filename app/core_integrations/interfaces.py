from abc import abstractmethod
from archtool.layers.default_layer_interfaces import ABCRepo

from lib.utils import get_settings_values


class LoggerRepoABC(ABCRepo):
    @abstractmethod
    async def log(self, log_data: list[dict[str, str]]) -> None:
        ...

    @abstractmethod
    def sync_log(self, log_data: list[dict[str, str]]) -> None:
        ...


class MinioRepoABC(ABCRepo):
    ...
