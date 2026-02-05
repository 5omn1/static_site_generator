import os
import shutil


def copy_dir_recursive(src_dir: str, dest_dir: str) -> None:
    if not os.path.isdir(src_dir):
        raise ValueError(f"Source directory does not exist: {src_dir}")

    # Create dest dir if it doesn't exist (this is why public/ not existing is OK)
    os.makedirs(dest_dir, exist_ok=True)

    # Delete everything inside dest dir (clean build)
    for name in os.listdir(dest_dir):
        path = os.path.join(dest_dir, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    # Recursively copy
    def _copy(cur_src: str, cur_dest: str) -> None:
        os.makedirs(cur_dest, exist_ok=True)

        for name in os.listdir(cur_src):
            src_path = os.path.join(cur_src, name)
            dest_path = os.path.join(cur_dest, name)

            if os.path.isdir(src_path):
                _copy(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {src_path} -> {dest_path}")

    _copy(src_dir, dest_dir)
