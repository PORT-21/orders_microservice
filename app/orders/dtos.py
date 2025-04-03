from typing import Optional
from uuid import UUID

from pydantic import Field
from lib.dtos import Base
from lib.types import UNSET, Unset

from . import enums


class SendTGMessageDTO(Base):
    content: str
    tg_chat_id: str


class RecievedTGMessageDTO(Base):
    tg_chat_id: str
    content: str
    sender: enums.SendersEnum


class SendChatMessage(Base):
    chat_id: UUID
    content: str


class Message(Base):
    ...


class CreateOrderDTO(Base):
    tg_chat_id: str
    chat_id: UUID
    details: dict
    status: enums.OrderStatusEnum


class FilterOrdersDTO(Base):
    chat_id: UUID | Unset = UNSET
    tg_chat_id: str | Unset = UNSET
    status: enums.OrderStatusEnum | Unset = UNSET


class FilterPositionsDTO(Base):
    ...


class OrderDTO(Base):
    ...


class CreateChatDTO(Base):
    tg_chat_id: int
    client_data: Optional[dict] = Field(default={})


class ChatDTO(Base):
    ...


class AddPositionDTO(Base):
    chat_id: UUID
    position_data: list[dict]


class RemovePositionDTO(Base):
    ...
