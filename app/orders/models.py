from typing import Optional, Any
from uuid import uuid4, UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lib.db import Base, Dated, create_enum_column
from . import enums 


class Message(Dated, Base):
    __tablename__ = "messages"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), index=True)
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    tg_message_id: Mapped[Optional[int]]
    content: Mapped[str]
    # attachments: Mapped[list[str]]
    sender: Mapped[enums.SendersEnum] = mapped_column(create_enum_column(enums.SendersEnum))

    def __repr__(self):
        return f"Message(id={self.id}, chat_id={self.chat_id})"

    def __str__(self):
        return f"Message(id={self.id}, chat_id={self.chat_id})"


class Chat(Dated, Base):
    __tablename__ = "chats"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    tg_chat_id: Mapped[int]
    messages: Mapped[list["Message"]] = relationship(back_populates="chat")
    orders: Mapped[list["Order"]] = relationship(back_populates="chat", uselist=True)

    client_data: Mapped[Optional[dict[str, Any]]] = mapped_column()

    def __repr__(self):
        return f"Chat(id={self.id}, tg_chat_id={self.tg_chat_id})"

    def __str__(self):
        return f"Chat(id={self.id}, tg_chat_id={self.tg_chat_id})"


class Positions(Base):
    __tablename__ = "positions"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    order_id: Mapped[UUID] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), index=True)
    order: Mapped["Order"] = relationship(back_populates="positions")
    composite_id: Mapped[str] = mapped_column(index=True)
    vendor_id: Mapped[int]
    position_data: Mapped[dict[str, Any]] = mapped_column(default={})

    def __repr__(self):
        return f"Position(id={self.id}, order_id={self.order_id})"

    def __str__(self):
        return f"Position(id={self.id}, order_id={self.order_id})"


class Order(Dated, Base):
    __tablename__ = "orders"
    id: Mapped[UUID] = mapped_column(primary_key=True, index=True, default=uuid4)
    tg_chat_id: Mapped[int]
    # messages: Mapped[list["Message"]] = relationship(back_populates="order")
    chat_id: Mapped[UUID] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"), index=True)
    chat: Mapped["Chat"] = relationship(back_populates="orders", uselist=False)

    details: Mapped[dict[str, Any]] = mapped_column(default={})
    status: Mapped[enums.OrderStatusEnum] = mapped_column(create_enum_column(enums.OrderStatusEnum), default=enums.OrderStatusEnum.NEW)
    positions: Mapped[list[Positions]] = relationship(back_populates="order")

    def __repr__(self):
        return f"Order(id={self.id}, tg_chat_id={self.tg_chat_id})"

    def __str__(self):
        return f"Order(id={self.id}, tg_chat_id={self.tg_chat_id})"
