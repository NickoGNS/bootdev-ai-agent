import os
import subprocess

def run_python_file(working_dir, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_dir)

        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if (
            not os.path.commonpath([target_file_path, working_dir_abs])
            == working_dir_abs
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args:
            command.extend(args)

        sp = subprocess.run(command, capture_output=True, text=True, timeout=30)

        if sp.returncode != 0:
            return f"Process exited with code {sp.returncode}"

        if not sp.stdout and not sp.stderr:
            return "No output produced"

        return f"STDOUT: {sp.stdout}, STDERR: {sp.stderr}"

    except Exception as err:
        return f"Error: executing Python file: {err}"
