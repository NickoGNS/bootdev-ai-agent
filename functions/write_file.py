import os
from google.genai import types

def write_file(working_dir, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if (
            not os.path.commonpath([target_file_path, working_dir_abs])
            == working_dir_abs
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{target_file_path}" ({len(content)} characters written)'

    except Exception as err:
        return f"Error: {err}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a given file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of the file to write content, relative to the working directory (default is the working directory itself), also creates path's folders if they don't exist",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="New content to replace of provided file",
            ),
        },
    ),
)
