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
    print(f"[DevDoc AI] -> {msg}")