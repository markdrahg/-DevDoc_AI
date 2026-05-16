class Reasoning:

    def refine_query(self, query: str) -> str:
        return query.strip()

    def post_process(self, response: str) -> str:
        return response.strip()