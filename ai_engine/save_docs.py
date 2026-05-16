import os
from typing import List, Dict, Any


def save_docs(chunks: List[Dict], doc_generator) -> None:
    output_dir = "docs"
    os.makedirs(output_dir, exist_ok=True)

    saved_files = 0
    seen_files: set[Any] = set()

    for chunk in chunks:
        file_path = chunk["file_path"]

        if file_path in seen_files:
            continue

        seen_files.add(file_path)

        try:
            doc = doc_generator.generate_for_chunk(chunk)

            file_name = os.path.basename(file_path) + ".md"
            output_path = os.path.join(output_dir, file_name)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(doc)

            saved_files += 1

        except Exception as e:
            print(f"⚠️ Skipped {file_path}: {e}")

    print(f"\n✅ Saved {saved_files} files in /docs/")