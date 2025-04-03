from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.orders import enums
from lib.dtos import Paginataion

from . import dtos
from .interfaces import (
    ChatRoutesInitializerABC,
    ChatServiceABC,
    ChatViewABC,
    OrdersRoutesInitializerABC,
    OrdersServiceABC,
    OrdersViewABC,
)


class ChatRoutesInitializer(ChatRoutesInitializerABC):
    router = APIRouter(prefix="/chat", tags=['chat'])
    chat_view: ChatViewABC

    def __call__(self):
        self.router.add_api_route("/send_message", self.chat_view.send_message, methods=["POST"], operation_id="send_message")
        self.router.add_api_route("/get_chat_history", self.chat_view.get_chat_history, methods=["POST"], operation_id="get_chat_history")
        self.router.add_api_route("/find_messages", self.chat_view.find_messages, methods=["POST"], operation_id="find_messages")


class OrdersRoutesInitializer(OrdersRoutesInitializerABC):
    router = APIRouter(prefix="/orders", tags=['orders'])
    orders_view: OrdersViewABC

    def __call__(self):
        self.router.add_api_route("/create_order", self.orders_view.create_order, methods=["POST"], operation_id="create_order")
        self.router.add_api_route("/set_order_status", self.orders_view.set_order_status, methods=["PATCH"], operation_id="set_order_status")
        self.router.add_api_route("/filter_orders", self.orders_view.filter_orders, methods=["POST"], operation_id="filter_orders")
        self.router.add_api_route("/get_order", self.orders_view.get_order, methods=["GET"], operation_id="get_order")
        self.router.add_api_route("/add_positions", self.orders_view.add_positions, methods=["POST"], operation_id="add_positions")
        self.router.add_api_route("/delete_positions", self.orders_view.delete_positions, methods=["DELETE"], operation_id="delete_positions")


class ChatView(ChatViewABC):
    # @app.get("/join_chat/{chat_id}")
    # async def join_chat(chat_id: UUID):
    #     """
    #     Присоединение к чату (получение токена для Centrifugo).
    #     """
    #     if chat_id not in chats:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Чат не найден")

    #     # Генерируем токен для клиента Centrifugo
    #     user_id = tg_chat_id
    #     channel_name = f"chat:{chat_id}"

    #     token_data = {
    #         "user": user_id,
    #         "channels": [channel_name],
    #         "exp": int((datetime.utcnow() + timedelta(minutes=30)).timestamp()),  # Время истечения токена
    #     }

    #     token = centrifuge_client.generate_token(token_data)
    #     return {"token": token, "user_id": user_id, "channel_name": channel_name}

    async def send_message(self, message: dtos.SendChatMessage) -> None:
        await self.send_message(message)

    async def get_chat_history(self, chat_id: UUID, pagination: Paginataion=Depends()) -> list[dtos.Message]:
        return await self.get_chat_history()

    async def find_messages(self, chat_id: UUID, substring=None, regex=None):
        return await self.find_messages(chat_id=chat_id, substring=substring, regex=regex)



# TODO: добавить сериализацию
class OrdersView(OrdersViewABC):
        orders_service: OrdersServiceABC

        async def create_order(self, order: dtos.CreateOrderDTO) -> dtos.OrderDTO:
            result = await self.orders_service.create_order(order)

        async def set_order_status(self, order_id: int, status: enums.OrderStatusEnum) -> dtos.OrderDTO:
            await self.orders_service.set_order_status(order_id, status)
        
        async def filter_orders(self, payload: dtos.FilterOrdersDTO, pagination: Paginataion=Depends()) -> list[dtos.OrderDTO]:
            result = await self.orders_service.filter_orders(payload, pag_info=pagination)

        async def get_order(self, order_id: int) -> dtos.OrderDTO:
            result = await self.orders_service.get_order(order_id)
            return 

        async def add_positions(self, data: dtos.AddPositionDTO) -> None:
            await self.add_positions(data)

        async def delete_positions(self, ids: list[UUID]) -> None:
            await self.delete_positions(ids)
