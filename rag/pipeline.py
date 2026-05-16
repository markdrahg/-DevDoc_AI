from rag.granite_client import GraniteClient
from rag.prompt_templates import PromptTemplates
from rag.reasoning import Reasoning


class RAGPipeline:

    def __init__(self, retriever, context_builder):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm = GraniteClient()
        self.reasoning = Reasoning()

    def run(self, query: str):

        # 1️⃣ refine query
        refined_query = self.reasoning.refine_query(query)

        # 2️⃣ retrieve relevant chunks
        chunks = self.retriever.search(refined_query)

        if not chunks:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        # 3️⃣ build context
        context = self.context_builder.build(chunks)

        # 4️⃣ build prompt
        prompt = PromptTemplates.build(context, refined_query)

        # 5️⃣ generate response
        answer = self.llm.generate(prompt)

        # 6️⃣ post-process
        answer = self.reasoning.post_process(answer)

        return {
            "answer": answer,
            "sources": [c["file_path"] for c in chunks]
        }