from uuid import UUID
from lib.dtos import Base

from . import enums


class SendTGMessageDTO(Base):
    content: str
    tg_chat_id: str


class RecievedTGMessageDTO(Base):
    tg_chat_id: str
    content: str
    sender: enums.SenderEnum


class SendChatMessage(Base):
    chat_id: UUID
    


class Message(Base):
    ...


class CreateOrderDTO(Base):
    ...


class FilterOrdersDTO(Base):
    ...


class OrderDTO(Base):
    ...

