import uuid
from sqlmodel import Session, select
from app.domains.projects.models.project import Project


class ProjectRepository:
    # Stores a session for database operations
    def __init__(self, session: Session):
        self.session = session

    # Saves a project to the database
    def create(self, project: Project):
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    # Retrieves a project by its ID
    def get_by_id(self, project_id: str):
        return self.session.get(Project, project_id)

    # Retrieves a project by name for a specific user
    def get_by_name(self, user_id: uuid.UUID, repo_name: str):
        statement = select(Project).where(
            Project.user_id == user_id, Project.repo_name == repo_name
        )
        return self.session.exec(statement).first()

    # Retrieves all projects or projects belonging to one user
    def get_all(self, user_id: str):
        if user_id:
            statement = select(Project).where(Project.user_id == user_id)
        else:
            statement = select(Project)
        return self.session.exec(statement).all()

    # Updates a project and persists changes
    def update(self, project: Project):
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project

    # Deletes a project by ID
    def delete(self, project_id: str):
        project = self.session.get(Project, project_id)
        if project:
            self.session.delete(project)
            self.session.commit()
        return project
