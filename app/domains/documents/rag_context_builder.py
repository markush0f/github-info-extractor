class RagContextBuilder:
    def __init__(self):
        pass

    def build(self, query: str, results: list):
        # Added reconstruction of retrieved chunks as context text
        combined_chunks = "\n\n".join(
            [item["content"] for item in results]
        )

        # Added final context structure for the LLM
        context = f"""
Retrieved information:
{combined_chunks}

User question:
{query}
"""

        return context
