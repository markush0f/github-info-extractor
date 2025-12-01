from sqlmodel import Session, select, desc, asc
from sqlalchemy import text
from uuid import UUID
from app.domains.messages.models.message import Message


class MessageRepository:
    model_name = "Message"

    def __init__(self, session: Session):
        # Added DB session dependency
        self.session = session

    def create(self, message: Message) -> Message:
        # Added message persistence
        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def get_by_id(self, message_id: UUID) -> Message | None:
        # Added retrieval by PK
        return self.session.get(Message, message_id)


    def get_all_by_chat(self, chat_id: UUID) -> list[Message]:
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(asc(Message.created_at))
        )
        return list(self.session.exec(query).all())


    def get_last_n(self, chat_id: UUID, limit: int = 10):
        query = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        return self.session.exec(query).all()

    def delete_by_chat(self, chat_id: UUID):
        # Added deletion SQL
        sql = text(
            """
            DELETE FROM messages
            WHERE chat_id = :chat_id
        """
        )

        self.session.execute(sql, {"chat_id": str(chat_id)})
        self.session.commit()
