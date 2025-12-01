from uuid import UUID
import uuid
from app.core.db import get_session
from app.domains.chunks.service import ChunkService
from app.domains.documents.service import DocumentService
from app.domains.embeddings.service import EmbeddingService
from app.domains.entities.service import EntityService
from app.domains.projects.service import ProjectService
from app.domains.users.models.user import User
from app.infrastructure.repositories.user_repository import UserRepository
from app.shared.services.record_finder import RecordFinder
from app.core.logger import logger


class UserService:
    def __init__(self):
        self.session = get_session()
        self.user_repository = UserRepository(self.session)
        self.embedding_service = EmbeddingService()
        self.chunk_service = ChunkService()
        self.document_service = DocumentService()
        self.entity_service = EntityService()
        self.project_service = ProjectService()
        self.record_finder = RecordFinder(self.user_repository)
        
    def create_user(self, username, name, bio, avatar_url, github_username):
        existing = self.user_repository.get_by_username(username)
        if existing:
            self.session.close()
            return existing

        user = User(
            username=username,
            name=name,
            bio=bio,
            avatar_url=avatar_url,
            github_username=github_username,
        )

        result = self.user_repository.create(user)
        self.session.close()
        return result

    def get_user(self, user_id: str):
        result = self.user_repository.get_by_id(user_id)
        self.session.close()
        return result

    def list_users(self):
        result = self.user_repository.get_all()
        self.session.close()
        return result

    def get_user_by_github(self, github_username: str):
        user = self.user_repository.get_by_github_username(github_username)
        self.session.close()
        return user

    def get_user_by_id(self, id):
        user = self.user_repository.get_by_id(id)
        return user

    def get_user_or_404(self, user_id: UUID):
        return RecordFinder(self.user_repository).find_or_404(user_id)

    def delete_user_data(self, user_id: uuid.UUID):
        self.record_finder.find_or_404(user_id)
        logger.info(f"Starting full deletion for user {user_id}")

        try:
            self.session.begin()

            logger.info("Deleting embeddings")
            self.embedding_service.delete_all(user_id)

            logger.info("Deleting chunks")
            self.chunk_service.delete_all(user_id)

            logger.info("Deleting documents")
            self.document_service.delete_all(user_id)

            logger.info("Deleting entities")
            self.entity_service.delete_all(user_id)

            logger.info("Deleting projects")
            self.project_service.delete_all(user_id)

            self.session.commit()
            logger.info(f"Deletion successfully completed for user {user_id}")

        except Exception as error:
            logger.error(f"Error during deletion for user {user_id}: {error}")
            self.session.rollback()
            raise

        finally:
            self.session.close()

