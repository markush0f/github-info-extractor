from openai import OpenAI
from app.infrastructure.repositories.embedding_repository import EmbeddingRepository
from core.db import get_session


class VectorSearchService:
    def __init__(self):
        # Added OpenAI client
        self.client = OpenAI()

    async def search(self, query: str, user_id: str, top_k: int = 5):
        # Added embedding generation for the query
        query_embedding = self._embed(query)

        # Added repository usage inside session
        with get_session() as session:
            repo = EmbeddingRepository(session)
            results = repo.search(user_id, query_embedding, top_k)

        return results

    def _embed(self, text: str):
        # Added OpenAI embeddings generation
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
