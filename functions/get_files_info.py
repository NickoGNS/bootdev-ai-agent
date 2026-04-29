import os
from google.genai import types

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

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
