# processing/code_analyzer.py

import re

class CodeAnalyzer:

    def analyze(self, content):
        functions = re.findall(r"def\s+(\w+)\(", content)
        classes = re.findall(r"class\s+(\w+)", content)

        return {
            "functions": functions,
            "classes": classes,
            "has_functions": len(functions) > 0,
            "has_classes": len(classes) > 0
        }

    def detect_chunk_type(self, chunk):
        if "def " in chunk:
            return "function"
        elif "class " in chunk:
            return "class"
        else:
            return "code"