from typing import List, Dict


class ContextBuilder:

    def build(self, chunks: List[Dict]) -> str:

        if not chunks:
            return "No relevant context found."

        context_parts = []

        for i, chunk in enumerate(chunks):
            part = f"""
--- Source {i+1} ---
File: {chunk['file_path']}
Type: {chunk.get('chunk_type', 'unknown')}
Language: {chunk.get('language', 'unknown')}

{chunk['content']}
"""
            context_parts.append(part.strip())

        return "\n\n".join(context_parts)