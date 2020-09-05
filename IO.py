from json import load as jload, dump as jdump
from os import getcwd, path

def file_io(filepath, save_or_load, file_to_save = None):
    cwd = getcwd()
    full_path = path.join(cwd, filepath)
    if save_or_load == 'load':
        data = {}
        if path.isfile(full_path):
            with open(full_path) as f:
                data = jload(f)
        return data
    elif save_or_load == 'save':
        with open(full_path, 'w') as f:
            jdump(file_to_save, f)