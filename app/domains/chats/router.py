from fastapi import APIRouter
from uuid import UUID

from app.domains.chats.schemas.send_message_request import SendMessageRequest
from app.domains.chats.service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])

chat_service = ChatService()


@router.post("/create/{user_id}")
def create_chat(user_id: UUID):
    chat = chat_service.create_chat(user_id)
    return {"chat_id": chat.id}


@router.post("/send/{chat_id}/{user_id}")
async def send_message(chat_id: UUID, user_id: UUID, body: SendMessageRequest):
    reply = await chat_service.send_message(chat_id, user_id, body.message)
    return {"reply": reply}


@router.get("/{chat_id}")
def get_chat(chat_id: UUID):
    chat = chat_service.get_chat(chat_id)
    return chat
