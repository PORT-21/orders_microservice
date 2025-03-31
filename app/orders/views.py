from uuid import UUID

from fastapi import HTTPException
from .interfaces import ChatServiceABC, ChatViewABC



class ChatView(ChatViewABC):
    # @app.get("/join_chat/{chat_id}")
    async def join_chat(chat_id: UUID):
        """
        Присоединение к чату (получение токена для Centrifugo).
        """
        if chat_id not in chats:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Чат не найден")

        # Генерируем токен для клиента Centrifugo
        user_id = tg_chat_id
        channel_name = f"chat:{chat_id}"

        token_data = {
            "user": user_id,
            "channels": [channel_name],
            "exp": int((datetime.utcnow() + timedelta(minutes=30)).timestamp()),  # Время истечения токена
        }

        token = centrifuge_client.generate_token(token_data)
        return {"token": token, "user_id": user_id, "channel_name": channel_name}
