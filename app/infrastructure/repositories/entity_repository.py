import uuid
from app.domains.entities.models.entity import Entity
from sqlalchemy import text  

class EntityRepository:
    model_name = "Entity"
    def __init__(self, session):
        self.session = session

    def create(self, data: dict):
        entity = Entity(**data)
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_project(self, project_id):
        return (
            self.session.query(Entity)
            .filter(Entity.project_id == project_id)
            .first()
        )

    def get_by_id(self, entity_id: uuid.UUID):
        return self.session.get(Entity, entity_id)
    
    def delete_all_by_user(self, user_id: uuid.UUID):
        sql = text("""
            DELETE FROM documents
            USING entities
            WHERE documents.entity_id = entities.id
            AND entities.user_id = :user_id
        """)
        self.session.execute(sql, {"user_id": user_id})
        self.session.commit()