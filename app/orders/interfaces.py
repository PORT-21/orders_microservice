from typing import Any, Optional
from abc import  abstractmethod

from archtool.layers.default_layer_interfaces import ABCView, ABCController, ABCService, ABCRepo
from lib.dtos import Paginataion

from . import dtos
from . import enums


class ChatViewABC(ABCView):
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


class ChatServiceABC(ABCService):
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

    async def get_chat_history(self, chat_id, pag_info: Paginataion) -> list[dtos.Message]:
        """
        возвращает историю чата
        """
        ...



class TGBotServiceABC(ABCService):

    async def send_message(self, message: dtos.SendTGMessageDTO) -> None:
        """
        отправляет сообщение в чат с тг ботом
        """
        ...

    async def handle_message(self, update: dict[str, Any]) -> dtos.RecievedTGMessageDTO:
        """
        Обрабатывает входящее сообщение от тг бота
        """
        ...

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
