from app.domains.embeddings.models.embbeding import Embedding
from sqlalchemy import text


class EmbeddingRepository:
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
            {"ids": chunk_ids}
        )
        self.session.commit()

    def get_by_id(self, entity_id: str):
        return self.session.get(Embedding, entity_id)

    def search(self, user_id: str, query_embedding: list, top_k: int):
        # Added pgvector similarity search using <-> operator
        sql = text("""
            SELECT id, content, embedding <-> :query_embedding AS distance
            FROM embeddings
            WHERE user_id = :user_id
            ORDER BY embedding <-> :query_embedding
            LIMIT :top_k
        """)

        rows = self.session.execute(
            sql,
            {
                "query_embedding": query_embedding,
                "user_id": user_id,
                "top_k": top_k,
            }
        ).fetchall()

        # Added result normalization
        return [
            {"content": row.content, "distance": row.distance}
            for row in rows
        ]
