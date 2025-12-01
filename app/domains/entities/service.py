import uuid
from app.core.db import get_session
from app.infrastructure.repositories.entity_repository import EntityRepository
from app.core.logger import logger
from app.core.logger import logger


class EntityService:

    def __init__(self):
        self.session = get_session()
        self.entity_repository = EntityRepository(self.session)

    def create_entity(
        self,
        user_id: uuid.UUID,
        project_id: uuid.UUID | None,
        entity_type: str,
        raw_data: dict,
        summary: str,
    ):
        logger.info(f"Creating entity for project: {project_id}")

        entity_data = {
            "user_id": user_id,
            "project_id": project_id,
            "type": entity_type,
            "raw_data": raw_data,
            "summary": summary,
        }

        existing = self.entity_repository.get_by_project(project_id)
        if existing:
            return existing

        created = self.entity_repository.create(entity_data)
        return created  #

    def get_by_id(self, id):
        return self.entity_repository.get_by_id(id)
        
    
    def delete_all(self, user_id):
        self.entity_repository.delete_all_by_user(user_id)