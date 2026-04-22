import os


def get_files_info(working_dir, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        if not os.path.commonpath([target_dir, working_dir_abs]) == working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir}" is not a directory'

        for file in os.listdir(target_dir):
            return f"- {file}: file_size={file.__sizeof__()} bytes, is_dir={os.path.isdir(os.path.join(target_dir, file))}"
    except Exception as err:
        return f"Error: {err}"
