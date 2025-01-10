import time
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, BigInteger, Boolean
from database.db_init import JSONField

from database.connection import Base, get_db
from utils.helper_functions import get_custom_logger

log = get_custom_logger(name=__name__)


class Chat(Base):
    __tablename__ = "chats"

    id = Column(String(255), primary_key=True)
    chat = Column(JSONField)
    created_at = Column(BigInteger, default=lambda: int(time.time() * 1000))
    updated_at = Column(BigInteger, default=lambda: int(time.time() * 1000), onupdate=lambda: int(time.time() * 1000))
    is_deleted = Column(Boolean, default=False)


class ChatSchema(BaseModel):
    messages: list


class ChatModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True
    )

    id: str
    chat: ChatSchema
    created_at: int
    updated_at: int
    is_deleted: bool = False


class ChatForm(BaseModel):
    chat: ChatSchema


class ChatTable:
    def insert_new_chat(self, chat_id: str, chat: ChatSchema) -> Optional[ChatModel]:
        with get_db() as db:
            if not chat_id:
                log.error("Cannot Insert chat without ID. Insertion failed.")
                return None

            chat_id = str(chat_id)
            log.info(f"Inserting new chat with ID: {chat_id}")
            chat = ChatModel(
                **{
                    "id": chat_id,
                    "chat": chat,
                    "created_at": int(time.time()),
                    "updated_at": int(time.time()),
                }
            )

            result = Chat(**chat.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            return ChatModel.model_validate(result) if result else None

    @staticmethod
    def update_chat_by_id(chat_id: str, chat: ChatSchema) -> Optional[ChatModel]:
        try:
            with get_db() as db:
                chat_obj = db.get(Chat, chat_id)
                chat_obj.chat = chat
                chat_obj.updated_at = int(time.time())
                db.commit()
                db.refresh(chat_obj)

                log.info(f"Updated chat with ID: {chat_obj.id}")
                return ChatModel.model_validate(chat_obj)
        except Exception as e:
            log.exception(f"Unable to update chat. Error: {str(e)}")
            return None

    @staticmethod
    def get_chat_by_id(chat_id: str) -> Optional[ChatModel]:
        try:
            with get_db() as db:
                chat = db.get(Chat, chat_id)
                if chat:
                    log.info(f"Found chat with ID: {chat.id}")
                    return ChatModel.model_validate(chat)
                else:
                    log.info(f"Chat with ID: {chat_id} not found.")
                    return None
        except Exception as e:
            log.exception(f"Unable to get chat. Error: {str(e)}")
            return None


Chats = ChatTable()
