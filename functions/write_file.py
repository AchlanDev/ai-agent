
# Write content to a file

import os

def write_file(working_directory, file_path, content):

    try:
        abs_working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.join(abs_working_directory, file_path)

        if os.path.commonpath([full_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.dirname(full_file_path) != "":
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        with open(full_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Cannot write to "{file_path}" - {str(e)}'