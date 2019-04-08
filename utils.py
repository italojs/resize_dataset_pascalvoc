from pathlib import Path


def add_end_slash(path):
    if path[-1] is not '/':
        return path + '/'
    return path


def create_path(path):
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)


def get_file_name(path):
    path = path.split('/')
    base_dir = path[:len(path)-1]
    base_dir = '/'.join(str(x) for x in base_dir)
    names = path[-1].split('.')
    file_name = names[0]
    ext = names[1]
    return (base_dir, file_name, ext)
