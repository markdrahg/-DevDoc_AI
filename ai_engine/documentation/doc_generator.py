import os
from typing import List, Dict

# shared usage
from shared.utils import get_file_name, log


def build_doc_prompt(file_path, code):
    return f"""
You are an expert software engineer.

Analyze the code and generate HIGH QUALITY documentation.

IMPORTANT:
- If it's Python → extract real classes, functions, purpose
- If it's NOT code → summarize meaningfully (DO NOT return N/A)
- NEVER leave sections empty
- Be specific and useful

FORMAT:

Overview:
Explain what this file does clearly.

Responsibilities:
- List real responsibilities

Classes:
- List classes if present, else "None"

Functions:
- List functions if present, else "None"

Summary:
Short clear summary.

File: {file_path}

Code:
{code}
"""


class DocumentationGenerator:

    def __init__(self, llm):
        self.llm = llm

        path = os.path.join(
            os.path.dirname(__file__),
            "templates",
            "doc_template.md"
        )

        with open(path, "r", encoding="utf-8") as f:
            self.template = f.read()

    def generate_for_chunk(self, chunk):
        code = chunk["content"][:3000]
        path = chunk["file_path"]

        log(f"Generating doc for: {get_file_name(path)}")

        res = self.llm.generate(build_doc_prompt(path, code))

        sections = {
            "brief_description": "",
            "responsibilities_list": "",
            "classes_section": "",
            "functions_section": "",
            "summary_text": ""
        }

        key = None

        for line in res.split("\n"):
            line = line.strip()

            if line.lower().startswith("overview"):
                key = "brief_description"
                continue
            elif line.lower().startswith("responsibilities"):
                key = "responsibilities_list"
                continue
            elif line.lower().startswith("classes"):
                key = "classes_section"
                continue
            elif line.lower().startswith("functions"):
                key = "functions_section"
                continue
            elif line.lower().startswith("summary"):
                key = "summary_text"
                continue

            if key:
                sections[key] += line + "\n"

        return self.template.format(
            file_name=get_file_name(path),
            file_path=path,
            brief_description=sections["brief_description"] or "N/A",
            responsibilities_list=sections["responsibilities_list"] or "N/A",
            classes_section=sections["classes_section"] or "None",
            functions_section=sections["functions_section"] or "None",
            summary_text=sections["summary_text"] or "N/A",
            language="python",
            code_example=code,
            dependencies_list="N/A",
            usage_example="# example",
            related_files_list="N/A"
        )

    def generate(self, chunks) -> str:
        docs = []
        seen = {}

        log("Grouping chunks by file...")

        # group chunks by file
        for c in chunks:
            path = c["file_path"]
            if path not in seen:
                seen[path] = ""
            seen[path] += c["content"]

        log(f"Generating docs for {len(seen)} files...")

        for path, full_code in seen.items():
            chunk = {
                "file_path": path,
                "content": full_code[:5000]
            }
            docs.append(self.generate_for_chunk(chunk))

        log("Documentation generation complete")

        return "\n\n".join(docs)