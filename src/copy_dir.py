import os
import shutil


def copy_dir_recursive(src_dir, dest_dir, log=True):
    if not os.path.isdir(src_dir):
        raise ValueError(
            f"Source directory does not exist or is not directory: {src_dir}"
        )
    os.makedirs(dest_dir, exist_ok=True)
    for name in os.listdir(dest_dir):
        path = os.path.join(dest_dir, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def _copy(current_src, current_dest):
        os.makedirs(current_dest, exist_ok=True)
        for name in os.listdir(current_src):
            src_path = os.path.join(current_src, name)
            dest_path = os.path.join(current_dest, name)

            if os.path.isdir(src_path):
                _copy(src_path, dest_path)
            else:
                shutil.copy(src_path, dest_path)
                if log:
                    print(f"Copied {src_path} -> {dest_path}")
        _copy(src_dir, dest_dir)
