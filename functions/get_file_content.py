import os
from config import MAX_CHARS


def get_file_content(working_dir, file_path):
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if (
            not os.path.commonpath([target_file_path, working_dir_abs])
            == working_dir_abs
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return (
                f'Error: File not found or is not a regular file: "{target_file_path}"'
            )

        content = ""
        with open(target_file_path, "r") as f:
            content += f.read(MAX_CHARS)

            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content

    except Exception as err:
        return f"Error: {err}"
