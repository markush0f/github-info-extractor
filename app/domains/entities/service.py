import uuid
import httpx
from app.core.db import get_session
from app.infrastructure.repositories.entity_repository import EntityRepository
from app.core.logger import logger
from app.domains.documents.service import DocumentService
from app.core.config import HEADLESSX_API, HEADLESSX_AUTH_TOKEN
from app.core.logger import logger


class EntityService:
    def __init__(self):
        self.session = get_session()
        self.repository = EntityRepository(self.session)

    # Save an entity linked to a project
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

        existing = self.repository.get_by_project(project_id)
        if existing:
            return existing

        created = self.repository.create(entity_data)

        # Auto-generate document
        document_service = DocumentService()
        document = document_service.generate_document(created.id)

        return {"entity": created, "document_id": str(document.id)}  # type: ignore

    async def extract_web_info(self, url: str):
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                r = await client.get(
                    f"{HEADLESSX_API}/content",
                    params={"token": HEADLESSX_AUTH_TOKEN, "url": url},
                )
                return {"content": r.text}
        except httpx.ReadTimeout:
            return {"error": "ReadTimeout while requesting external API"}
        except Exception as e:
            return {"error": str(e)}
