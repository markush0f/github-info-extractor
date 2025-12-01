import uuid
from app.domains.embeddings.models.embbeding import Embedding
from sqlalchemy import text


class EmbeddingRepository:
    model_name = "Embedding"

    def __init__(self, session):
        self.session = session

    def create(self, item: Embedding):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def delete_by_chunk_ids(self, chunk_ids):
        if not chunk_ids:
            return
        self.session.execute(
            text("DELETE FROM embeddings WHERE chunk_id = ANY(:ids)"),
            {"ids": chunk_ids},
        )
        self.session.commit()

    def get_by_id(self, entity_id: str):
        return self.session.get(Embedding, entity_id)

    def search(self, user_id: str, query_embedding: list, top_k: int):
        # Convert list to pgvector format for CAST
        embedding_str = f"[{','.join(str(x) for x in query_embedding)}]"

        sql = text(
            """
            SELECT 
                e.id,
                c.chunk_text AS content,
                e.embedding <-> CAST(:query_embedding AS vector) AS distance
            FROM embeddings e
            JOIN chunks c ON e.chunk_id = c.id
            JOIN documents d ON c.document_id = d.id
            JOIN entities en ON d.entity_id = en.id
            WHERE en.user_id = :user_id
            ORDER BY e.embedding <-> CAST(:query_embedding AS vector)
            LIMIT :top_k
            """
        )

        rows = self.session.execute(
            sql,
            {
                "query_embedding": embedding_str,
                "user_id": user_id,
                "top_k": top_k,
            },
        ).fetchall()

        return [{"content": row.content, "distance": row.distance} for row in rows]


    def delete_all_by_user(self, user_id: uuid.UUID):
        sql = text("""
            DELETE FROM embeddings
            USING chunks, documents, entities
            WHERE embeddings.chunk_id = chunks.id
            AND chunks.document_id = documents.id
            AND documents.entity_id = entities.id
            AND entities.user_id = :user_id
        """)
        self.session.execute(sql, {"user_id": user_id})
        self.session.commit()
