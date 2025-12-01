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

@router.get("/user/{user_id}")
def get_chats_by_user(user_id: UUID):
    chats = chat_service.get_chats_by_user(user_id)
    return chats

@router.delete("/{chat_id}")
def delete_chat(chat_id: UUID):
    chat_service.delete_chat(chat_id)
    return {"deleted": True}

# 486f6d30-6431-4868-b24d-53490a710672
# 074fa34c-576f-483c-a37a-1b9fc15f0733