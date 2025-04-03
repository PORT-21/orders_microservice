from typing import Any, Optional
from abc import  abstractmethod
from uuid import UUID

from archtool.layers.default_layer_interfaces import ABCView, ABCController, ABCService, ABCRepo
from app.archtool_conf.custom_layers import RoutersInitializationStrategyABC
from lib.dtos import Paginataion

from . import dtos
from . import enums


class ChatRoutesInitializerABC(RoutersInitializationStrategyABC):
    @abstractmethod
    def __call__(self):
        ...


class OrdersRoutesInitializerABC(RoutersInitializationStrategyABC):
    @abstractmethod
    def __call__(self):
        ...


class ChatViewABC(ABCView):
    @abstractmethod
    async def send_message(self, message: dtos.SendChatMessage) -> None:
        ...

    @abstractmethod
    async def get_chat_history(self, chat_id, pag_info: Paginataion) -> list[dtos.Message]:
        """
        Возвращает историю чата
        """
        ...

    @abstractmethod
    async def find_messages(self, chat_id, substring: Optional[str] = None, regex: Optional[str] = None) -> list[dtos.Message]:
        """
        Поиск сообщений в чате 
        """
        ...
    # async def find_messages(self, chat_id: UUID, substring=None, regex=None):



class ChatServiceABC(ABCService):
    @abstractmethod
    async def create_chat(self, data: dtos.CreateChatDTO) -> dtos.ChatDTO:
        ...

    @abstractmethod
    async def send_message(self, message: dtos.SendChatMessage) -> None:
        """
        отправляет сообщение в чат с тг ботом
        """
        ...
    
    @abstractmethod
    async def handle_message(self, message: dtos.RecievedTGMessageDTO) -> None:
        """
        обрабатыватет сообщение
        """
        ...

    @abstractmethod
    async def get_chat_history(self, chat_id, pag_info: Paginataion) -> list[dtos.Message]:
        """
        возвращает историю чата
        """
        ...



class TGBotServiceABC(ABCService):
    @abstractmethod
    async def send_message(self, message: dtos.SendTGMessageDTO) -> None:
        """
        отправляет сообщение в чат с тг ботом
        """
        ...

    @abstractmethod
    async def handle_message(self, update: dict[str, Any]) -> dtos.RecievedTGMessageDTO:
        """
        Обрабатывает входящее сообщение от тг бота
        """
        ...

    @abstractmethod
    async def start_bot(self) -> None:
        """
        запускает обработку входящих сообщений от тг бота
        """
        ...


class OrdersServiceABC(ABCService):
    @abstractmethod
    async def create_order(self, order: dtos.CreateOrderDTO) -> dtos.OrderDTO:
        """
        создаёт объект заказа
        """
        ...

    @abstractmethod
    async def set_order_status(self, order_id: int, status: enums.OrderStatusEnum) -> dtos.OrderDTO:
        ...


    @abstractmethod
    async def filter_orders(self, payload: dtos.FilterOrdersDTO, pag_info: Paginataion) -> list[dtos.OrderDTO]:
        ...


    @abstractmethod
    async def get_order(self, order_id: int) -> dtos.OrderDTO:
        ...


class OrdersViewABC(ABCView):
        @abstractmethod
        async def create_order(self, order: dtos.CreateOrderDTO) -> dtos.OrderDTO:
            ...

        @abstractmethod
        async def set_order_status(self, order_id: int, status: enums.OrderStatusEnum) -> dtos.OrderDTO:
            ...
        
        @abstractmethod
        async def filter_orders(self, payload: dtos.FilterOrdersDTO, pag_info: Paginataion) -> list[dtos.OrderDTO]:
            ...

        @abstractmethod
        async def get_order(self, order_id: int) -> dtos.OrderDTO:
            ...

        @abstractmethod
        async def add_positions(self, data: dtos.AddPositionDTO) -> None:
            ...

        @abstractmethod
        async def delete_positions(self, ids: list[UUID]) -> None:
            ...
