import os


def get_files_info(working_dir, directory="."):
    working_dir_abs = os.path.abspath(working_dir)

    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

    if not os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory):
        f'Error: "{directory}" is not a directory'

    for file in os.listdir(directory):
        print(
            f"- {file}: file_size={file.__sizeof__()} bytes, is_dir={os.path.isdir(os.path.join(directory, file))}"
        )


get_files_info("../functions")
