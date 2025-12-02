import os
import uuid
from app.domains.documents.service import DocumentService
from app.domains.projects.models.project import Project
from app.infrastructure.repositories.project_repository import ProjectRepository
from app.domains.entities.service import EntityService
from app.domains.projects.summary_service import SummaryProjectsService
from app.infrastructure.github.github_files_loader import extract_projects
from app.core.logger import logger


class ProjectService:
    def __init__(self, session):
        self.session = session
        self.project_repository = ProjectRepository(self.session)
        self.entity_service = EntityService(self.session)
        self.document_service = DocumentService(self.session)
        self.summarizer = SummaryProjectsService()

    def create_project(
        self,
        user_id: uuid.UUID,
        repo_name: str,
        description: str,
        stars: int,
        forks: int,
        last_commit: str,
    ):
        project = Project(
            user_id=user_id,
            repo_name=repo_name,
            description=description,
            stars=stars,
            forks=forks,
            last_commit=last_commit,
        )

        self.project_repository.create(project)
        self.session.commit()
        return project

    def get_project(self, project_id: str):
        return self.project_repository.get_by_id(project_id)

    def list_projects(self, user_id: str):
        return self.project_repository.get_all(user_id)

    def update_project(self, project_id: str, **fields):
        project = self.project_repository.get_by_id(project_id)
        if not project:
            return None

        for key, value in fields.items():
            setattr(project, key, value)

        self.project_repository.update(project)
        self.session.commit()
        return project

    def delete_project(self, project_id: str):
        result = self.project_repository.delete(project_id)
        self.session.commit()
        return result

    def summarize_all_projects(self):
        return self.summarizer.summarize_all_projects()

    def save_all_projects(self, selection):
        logger.info("Loading project data from output")

        projects = extract_projects("output")
        results = []

        logger.info(f"Projects extracted: {len(projects)}")

        if selection and selection != "all":
            selection_normalized = [s.lower() for s in selection]
            projects = [
                p for p in projects if p["name"].lower() in selection_normalized
            ]
            logger.info(f"Projects after selection filter: {len(projects)}")

        if not projects:
            logger.warning("No projects to save from output")
            return {"saved": [], "total_saved": 0}

        for data in projects:
            logger.info(f"Saving project: {data['name']}")

            project_row = self._create_project_record(data)

            entity_row = self.entity_service.create_entity(
                user_id=project_row.user_id,
                project_id=project_row.id,
                entity_type="project_summary",
                raw_data={"project": data},
                summary=data.get("summary"),
            )

            document_row = self.document_service.generate_document(entity_row)

            results.append(
                {
                    "project_id": project_row.id,
                    "entity_id": entity_row.id,
                    "document_id": document_row.id,
                }
            )

        self.session.commit()
        logger.info(f"Saved {len(results)} projects/entities/documents")

        return {"saved": results, "total_saved": len(results)}

    def delete_all(self, user_id):
        self.project_repository.delete_all_by_user(user_id)
        self.session.commit()

    def _create_project_record(self, data: dict):
        existing = self.project_repository.get_by_name(
            data["user_id"],
            data["name"],
        )
        if existing:
            logger.info(f"Project already exists: {existing.repo_name}")
            return existing

        project = Project(
            user_id=data["user_id"],
            repo_name=data["name"],
            description=data.get("description", ""),
            stars=data.get("stars", 0),
            forks=data.get("forks", 0),
            last_commit=data.get("last_commit"),
        )

        self.project_repository.create(project)
        logger.info(f"New project created: {project.repo_name}")
        return project
