class PromptTemplates:

    @staticmethod
    def build(context, query):
        return f"""
You are an expert software engineer.

Analyze the following codebase and answer the question clearly.

Context:
{context}

Question:
{query}

Instructions:

- Use ONLY the provided context
- Be clear and confident
- Do NOT say "not enough information" unless context is empty

- If the context includes CONFIG or DATA files (.json, .yaml, .yml):
  → Explain the structure of the data
  → Describe key fields and their purpose
  → Explain how this data might be used in the project

- If the context includes CODE files:
  → Explain functionality and logic

Answer:
"""