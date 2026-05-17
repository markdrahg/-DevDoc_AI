class DocumentationHealthScorer:

    def score(self, chunks):
        total = len(chunks)
        
        # Handle empty chunks
        if total == 0:
            return {
                "score": 0.0,
                "coverage": 0.0,
                "comments": 0.0
            }
        
        funcs = 0
        comments = 0

        for c in chunks:
            txt = c["content"]

            if "def " in txt or "class " in txt:
                funcs += 1

            if "#" in txt or '"""' in txt:
                comments += 1

        coverage = (funcs / total) * 100
        comment_score = (comments / total) * 100

        final = (coverage * 0.6) + (comment_score * 0.4)

        return {
            "score": round(final, 2),
            "coverage": round(coverage, 2),
            "comments": round(comment_score, 2)
        }