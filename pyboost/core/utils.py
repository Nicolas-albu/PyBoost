from pathlib import Path


def get_path_name() -> str:
    return Path().cwd().name
