from typing import Any
from uuid import UUID

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import Router, F
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.orders.models import Chat, Order, Positions
from lib.db import paginate
from lib.dtos import Paginataion

from .interfaces import ChatServiceABC, TGBotServiceABC, OrdersServiceABC
from . import dtos, enums


keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Посмотреть историю заказов"),
               KeyboardButton(text="Оформить заказ")]], resize_keyboard=True)


class TGBotService(TGBotServiceABC):
    bot: Bot
    dp: Dispatcher
    chat_service: ChatServiceABC

    async def send_message(self, message: dtos.SendTGMessageDTO) -> None:
        """
        отправляет сообщение в чат с тг ботом
        """
        await self.bot.send_message(chat_id=message.tg_chat_id, text=message.content)


    async def handle_message(self, message: types.Message) -> dtos.RecievedTGMessageDTO:
        """
        Обрабатывает входящее сообщение от тг бота
        """
        # Создаём объект RecievedMessageDTO
        recieved_message_dto = dtos.RecievedTGMessageDTO(
            tg_chat_id=str(message.chat.id),
            content=message.text,
            sender=enums.SendersEnum.USER,
            timestamp=message.date.isoformat() if message.date else None,
        )
        return recieved_message_dto

    async def start_bot(self) -> None:
        # добавляем все обработчики сообщений для бота
        self.dp.message(Command('start'))(self.start_command)
        self.dp.message(F.text.lower() == 'оформить заказ')(self.create_order_handler)
        self.dp.message()(self.echo_handler)
        # Запускаем бота
        await self.dp.start_polling(self.bot)

    async def start_command(self, message: types.Message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name

        # Проверяем, является ли это первым взаимодействием
        if not await self.chat_service.is_chat_exist(message.chat.id):
            await self.bot.send_message(
                user_id,
                f"Привет, {first_name}!\n"
                "Продолжая работу с ботом, вы соглашаетесь на хранение и обработку персональных данных.",
                reply_markup=keyboard
            )
            await self.chat_service.create_chat(data=dtos.CreateChatDTO(tg_chat_id=message.chat.id, client_data={}))  # Регистрируем пользователя
        else:
            await self.bot.send_message(
                user_id,
                f"Рад снова видеть тебя, {first_name}!",
                reply_markup=keyboard
            )

    async def create_order_handler(self, message: types.Message) -> None:
        # позиции размеры
        # TODO: Город, позиция, размер, марка стали, количество
        await self.bot.send_message(chat_id=message.chat.id, text=(
            "Напишите пожалуйста информацию для менеджера: \n"
            "какие изделия вас интересуют? \n Уточните размеры"))

    async def echo_handler(self, message: types.Message) -> None:
        # Получаем входящее сообщение
        recieved_dto = await self.handle_message(message)
        print(f"Получено сообщение: {recieved_dto.content} от {recieved_dto.sender}")

        # Отправляем ответное сообщение
        response_message = dtos.SendTGMessageDTO(
            tg_chat_id=recieved_dto.tg_chat_id,
            content=f"Вы сказали: {recieved_dto.content}"
        )
        await self.send_message(response_message)



class ChatService(ChatServiceABC):
    sessionmaker: async_sessionmaker

    async def create_chat(self, data: dtos.CreateChatDTO) -> Chat:
        new_chat_obj = Chat(tg_chat_id=data.tg_chat_id, client_data=data.client_data)
        async with self.sessionmaker() as session:
            session.add(new_chat_obj)
            await session.commit()
            return new_chat_obj        

    async def is_chat_exist(self, chat_id) -> bool:
        chat_q = select(Chat).where(Chat.tg_chat_id == chat_id)
        async with self.sessionmaker() as session:
            chat = (await session.execute(chat_q)).scalars().first()
            return bool(chat)

    async def send_message(self, message: dtos.SendChatMessage) -> None:
        # TODO:
        ...


    async def handle_message(self, message: dtos.RecievedTGMessageDTO) -> None:
        """
        обрабатыватет сообщение
        """
        # TODO:

    async def get_chat_history(self, chat_id, pag_info: Paginataion) -> list[dtos.Message]:
        """
        возвращает историю чата
        """
        # TODO:
        ...


from sqlalchemy.ext.asyncio import AsyncSession


class OrdersService(OrdersServiceABC):
    sessionmaker: async_sessionmaker

    async def create_order(self, order: dtos.CreateOrderDTO) -> Order:
        """
        создаёт объект заказа
        """
        new_order = Order(
            tg_chat_id=order.tg_chat_id,
            chat_id=order.chat_id,
            # chat,
            details=order.details,
            status=enums.OrderStatusEnum.NEW,
        )
        async with self.sessionmaker() as session:
            session.add(new_order)
            await session.commit()
            return new_order

    async def add_positions(self, data: dtos.AddPositionDTO):
        get_order_q = select(Order).where(Order.id == data.order_id)
        async with self.sessionmaker() as session:
            order = session.execute(get_order_q).scalars().first()
            for position in data.positions:
                new_position = Positions(
                    order_id=order.id,
                    composite_id=position.composite_id,
                    vendor_id=position.vendor_id,
                    position_data=position.position_data,
                )
                session.add(new_position)
            await session.commit()

    async def delete_positions(self, ids: list[UUID]):
        async with self.sessionmaker() as session:
            delete_q = delete(Positions).where(Positions.id.in_(ids))
            session.execute(delete_q)
            await session.commit()

    async def set_order_status(self, order_id: int, status: enums.OrderStatusEnum) -> None:
        async with self.sessionmaker() as session:
            update_order_q = update(Order).where(Order.id == order_id).values(status=status)
            session.execute(update_order_q)
            await session.commit()

    async def filter_orders(self, payload: dtos.FilterOrdersDTO, pag_info: Paginataion) -> list[dtos.OrderDTO]:
        q = select(Order).where(payload.not_blank())
        paginated_q = paginate(q, pag_info)         
        async with self.sessionmaker() as session:
            orders = session.execute(paginated_q).scalars().all()
        return orders

    async def get_order(self, order_id: int) -> Order:
        q = select(Order).where(Order.id == order_id)
        async with self.sessionmaker() as session:
            order = session.execute(q).scalars().first()
        return order
