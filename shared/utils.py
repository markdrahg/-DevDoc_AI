import os


def clean_path(path: str) -> str:
    return path.replace("\\", "/")


def get_file_name(path: str) -> str:
    return os.path.basename(path)


def is_code_file(path: str) -> bool:
    return path.lower().endswith((
        ".py", ".js", ".ts", ".java", ".cpp", ".c"
    ))
    
def log(msg: str):
    # Handle Unicode encoding issues on Windows
    try:
        print(f"[DevDoc AI] -> {msg}")
    except UnicodeEncodeError:
        # Fallback: encode to ASCII, replacing problematic characters
        safe_msg = msg.encode('ascii', 'replace').decode('ascii')
        print(f"[DevDoc AI] -> {safe_msg}")