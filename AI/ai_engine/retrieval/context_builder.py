from typing import List, Dict


class ContextBuilder:
    def build(self, chunks):
        context = ""

        for c in chunks:
            context += f"\nFile: {c['file_path']}\n"
            context += c["content"] + "\n"

        return context