class PromptTemplates:

    @staticmethod
    def build(context: str, question: str) -> str:
        return f"""
You are an expert software engineer.

Answer the question using ONLY the provided context.
If the answer is not present, say: "Not enough information."

Context:
{context}

Question:
{question}

Give a clear, structured, technical answer.
"""