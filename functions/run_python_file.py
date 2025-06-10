
# Run python file using AI Agent

import os
import subprocess

def run_python_file(working_directory, file_path):

    try:
        abs_working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.abspath(os.path.join(abs_working_directory, file_path))

        if os.path.commonpath([full_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_file_path):
            return f'Error: File "{file_path}" not found.'

        if not full_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        processing = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            cwd=working_directory,
            timeout=30,
            check=False,
            text=True
        )

        output = f"STDOUT: {processing.stdout}\nSTDERR: {processing.stderr}"

        if not processing.stdout and not processing.stderr:
            return "No output produced."

        if processing.returncode != 0:
            output += f"\nProcess exited with code {processing.returncode}"

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"