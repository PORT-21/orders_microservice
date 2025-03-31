from typing import Any

from aiogram import Bot, Dispatcher, types
from fastapi import HTTPException

from .interfaces import ChatServiceABC, TGBotServiceABC
from . import dtos, enums


class TGBotService(TGBotServiceABC):
    bot: Bot
    dp: Dispatcher

    async def send_message(self, message: dtos.SendTGMessageDTO) -> None:
        """
        отправляет сообщение в чат с тг ботом
        """
        await self.bot.send_message(chat_id=message.tg_chat_id, text=message.content)


    async def handle_message(self, update: dict[str, Any]) -> dtos.RecievedTGMessageDTO:
        """
        Обрабатывает входящее сообщение от тг бота
        """
        tg_message = types.Message.to_object(update["message"])

        # Создаём объект RecievedMessageDTO
        recieved_message_dto = dtos.RecievedTGMessageDTO(
            tg_chat_id=str(tg_message.chat.id),
            content=tg_message.text,
            sender=enums.SenderEnum,
            timestamp=tg_message.date.isoformat() if tg_message.date else None,
        )
        return recieved_message_dto


    async def start_bot(self) -> None:
        @self.dp.message()
        async def echo_handler(message: types.Message) -> None:
            # Получаем входящее сообщение
            recieved_dto = await self.handle_message(message.to_python())
            print(f"Получено сообщение: {recieved_dto.content} от {recieved_dto.sender}")

            # Отправляем ответное сообщение
            response_message = dtos.SendTGMessageDTO(
                tg_chat_id=recieved_dto.tg_chat_id,
                content=f"Вы сказали: {recieved_dto.content}"
            )
            await self.send_message(response_message)

        # Запускаем бота
        await self.dp.start_polling(self.bot)


class ChatService(ChatServiceABC):
    async def send_message(self, message: str) -> None:
        ...
