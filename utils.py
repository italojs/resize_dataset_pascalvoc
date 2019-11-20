import os
from pathlib import Path


def add_end_slash(path):
    if path[-1] is not '/':
        return path + '/'
    return path


def create_path(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)


def get_file_name(path):
    base_dir = os.path.dirname(path)
    file_name, ext = os.path.splitext(os.path.basename(path))
    ext = ext.replace(".", "")
    return (base_dir, file_name, ext)
