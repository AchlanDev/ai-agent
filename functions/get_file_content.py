
# Get file content for AI Agent

import os

def get_file_content(working_directory, file_path):
    
    try:

        abs_working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.join(abs_working_directory, file_path)

        if os.path.commonpath([full_file_path, abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

    except Exception:
        return f'Error: Cannot read "{file_path}" - file does not exist or is inaccessible'

    MAX_CHARS = 10000

    try:
        
        with open(full_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if len(file_content_string) == MAX_CHARS:
                file_content_string = (
                    file_content_string +
                    f'[...File "{file_path}" truncated at 10000 characters]'
                )
            return file_content_string

    except Exception:
        return f'Error: Cannot read "{file_path}" - file does not exist or is inaccessible'