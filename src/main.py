import shutil
import os

from src.gencontent import generate_pages_recursive

static_dir_path = "./static"
public_dir_path = "./public"


def copy_files_to_dir(input, output):
    for file in os.listdir(input):
        relative_path = os.path.join(input, file)
        output_path = os.path.join(output, file)
        if os.path.isfile(relative_path):
            print(f"Copying file {relative_path} to {output_path}")
            shutil.copy(relative_path, output_path)
        else:
            print(f"Creating path {output_path}")
            os.mkdir(output_path)
            copy_files_to_dir(relative_path, output_path)


def setup_public_dir(input_dir, output_dir):
    if not os.path.isdir(input_dir):
        raise Exception("Invalid input dir is not a dir")
    if not os.path.exists(input_dir):
        raise Exception("Invalid input dir does not exist")
    if os.path.exists(output_dir):
        print(f"Clearing directory {output_dir}")
        shutil.rmtree(output_dir)
    print(f"Create {output_dir} directory")
    os.mkdir(output_dir)
    copy_files_to_dir(input_dir, output_dir)
    generate_pages_recursive("content/", "template.html", "public/")


def main():
    setup_public_dir(static_dir_path, public_dir_path)


main()
