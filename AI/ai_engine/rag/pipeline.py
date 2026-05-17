from ai_engine.rag.granite_client import GraniteClient
from ai_engine.rag.prompt_templates import PromptTemplates
from ai_engine.rag.reasoning import Reasoning


class RAGPipeline:

    def __init__(self, retriever, context_builder):
        self.retriever = retriever
        self.context_builder = context_builder
        self.llm = GraniteClient()
        self.reasoning = Reasoning()

    def run(self, query: str):

        # 1. refine query
        refined_query = self.reasoning.refine_query(query)

        # 2. retrieve relevant chunks
        chunks = self.retriever.search(refined_query)

        if not chunks:
            return {
                "answer": "No relevant information found.",
                "sources": []
            }

        # 3. build context
        context = self.context_builder.build(chunks)

        # 4. build prompt
        prompt = PromptTemplates.build(context, refined_query)

        # 5. generate response
        answer = self.llm.generate(prompt)

        # ensure string
        if not isinstance(answer, str):
            answer = str(answer)
        
        answer = self.reasoning.post_process(answer)
        return {
            "answer": answer,
            "sources": [c["file_path"] for c in chunks]
        }