import os
import shutil


def clean_dir(path: str) -> None:
    files = os.listdir(path)
    for file in files:
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            print(f"Deleting file: {full_path}")
            os.unlink(full_path)
        elif os.path.isdir(full_path):
            print(f"Deleting directory: {full_path}")
            shutil.rmtree(full_path)


def copy_dir(src: str, dst: str) -> None:
    if not (os.path.exists(src) and os.path.exists(dst)):
        raise ValueError("Path does not exist")

    # It should first delete all the contents of the destination directory to ensure that the copy is clean.
    print(f"Removing all file and directories from {src}")
    clean_dir(dst)

    to_copy = os.listdir(src)
    for file in to_copy:
        full_path = os.path.join(src, file)
        if os.path.isfile(full_path):
            full_dst = os.path.join(dst, file)
            print(f"Copying {full_path} to {full_dst}")
            shutil.copy(full_path, full_dst)
        elif os.path.isdir(full_path):
            full_dst = os.path.join(dst, file)
            os.mkdir(full_dst)
            copy_dir(full_path, full_dst)


def main() -> None:
    copy_dir("./static", "./public")


if __name__ == "__main__":
    main()
