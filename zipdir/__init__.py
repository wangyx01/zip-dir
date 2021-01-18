import os
import tempfile
import zipfile
import pathlib


def zip_directory(directory, output=None, compression=zipfile.ZIP_STORED):
    save_cwd = os.getcwd()
    if not os.path.isdir(directory):
        raise Exception(f"{directory} not a directory")
    os.chdir(directory)
    base_dir = os.curdir
    try:
        with tempfile.NamedTemporaryFile(
                prefix='zipdir_', suffix='zip'
        ) as named_temp:
            with zipfile.ZipFile(
                    named_temp.name, "w", compression=compression
            ) as zf:
                path = os.path.normpath(base_dir)
                if path != os.curdir:
                    zf.write(path, path)
                for dirpath, dirnames, filenames in os.walk(base_dir):
                    for name in sorted(dirnames):
                        path = os.path.normpath(os.path.join(dirpath, name))
                        zf.write(path, path)
                    for name in filenames:
                        path = os.path.normpath(os.path.join(dirpath, name))
                        if os.path.isfile(path):
                            zf.write(path, path)
            data = pathlib.Path(named_temp.name).read_bytes()
    finally:
        os.chdir(save_cwd)
    if output is not None:
        pathlib.Path(output).write_bytes(data)
    else:
        return data
