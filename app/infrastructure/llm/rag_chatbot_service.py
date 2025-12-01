from openai import OpenAI
from app.shared.utils.rag_context_builder import RagContextBuilder
from domains.embeddings.vector_search_service import VectorSearchService


class RagChatbotService:
    def __init__(self):
        # OpenAI client initialization
        self.client = OpenAI()

        # vector search and context builder services
        self.search_service = VectorSearchService()
        self.context_builder = RagContextBuilder()

    async def chat(self, user_id: str, message: str):
        #  retrieval step from the vector database
        retrieved_chunks = await self.search_service.search(message, user_id)

        # context construction using retrieved chunks
        context = self.context_builder.build(message, retrieved_chunks)

        prompt = f"""
            You are an assistant that must answer using only the provided context.
            If the information is not in the context, reply that you do not know.

            Context:
            {context}
            """

        completion = self.client.chat.completions.create(
            model="gpt-4.1-mini", messages=[{"role": "user", "content": prompt}]
        )

        return completion.choices[0].message.content
