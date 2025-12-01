from uuid import UUID, uuid4
from app.domains.chats.models.chat import Chat
from app.domains.messages.models.message import Message
from app.core.db import get_session

from app.infrastructure.repositories.chat_repository import ChatRepository
from app.infrastructure.repositories.message_repository import MessageRepository
from app.domains.embeddings.vector_search_service import VectorSearchService
from app.shared.utils.rag_context_builder import RagContextBuilder
from app.infrastructure.llm.llm_client import LLMClient


class ChatService:
    def __init__(self):
        self.session = get_session()
        self.chat_repo = ChatRepository(self.session)
        self.message_repo = MessageRepository(self.session)
        self.vector_service = VectorSearchService()
        self.context_builder = RagContextBuilder()
        self.llm = LLMClient()

    def create_chat(self, user_id: UUID) -> Chat:
        chat = Chat(id=uuid4(), user_id=user_id)
        return self.chat_repo.create(chat)

    def delete_chat(self, chat_id: UUID):
        return self.chat_repo.delete(chat_id)

    def get_chat(self, chat_id: UUID) -> Chat | None:
        return self.chat_repo.get_by_id(chat_id)

    async def send_message(self, chat_id: UUID, user_id: UUID, content: str) -> str:
        chat = self._ensure_chat(chat_id, user_id)
        self._store_user_message(chat.id, content)

        history = self.message_repo.get_last_n(chat.id, limit=10)
        rag_context = await self._create_rag_context(content, user_id)
        prompt = self._create_prompt(history, rag_context, content)

        assistant_reply = self.llm.generate(prompt)
        self._store_assistant_message(chat.id, assistant_reply)

        return assistant_reply

    def _ensure_chat(self, chat_id: UUID, user_id: UUID) -> Chat:
        chat = self.chat_repo.get_by_id(chat_id)
        if chat:
            return chat
        return self.create_chat(user_id)

    def _store_user_message(self, chat_id: UUID, content: str):
        msg = Message(id=uuid4(), chat_id=chat_id, role="user", content=content)
        self.message_repo.create(msg)

    def _store_assistant_message(self, chat_id: UUID, content: str):
        msg = Message(id=uuid4(), chat_id=chat_id, role="assistant", content=content)
        self.message_repo.create(msg)

    async def _create_rag_context(self, content: str, user_id: UUID) -> str:
        chunks = await self.vector_service.search(content, str(user_id))
        return self.context_builder.build(content, chunks)

    def _create_prompt(
        self, history: list[Message], rag_context: str, user_input: str
    ) -> str:
        history_text = "\n".join(f"{m.role.upper()}: {m.content}" for m in history)

        return f"""
            You are a contextual assistant. Use conversation history and retrieved context.
            If the answer is not in the context, say you do not know.

            Conversation history:
            {history_text}

            Retrieved context:
            {rag_context}

            User message:
            {user_input}
            """
