
# Get file information for AI Agent

import os

def get_files_info(working_directory, directory=None):

    if directory is None:
        directory = "."

    full_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    
    if os.path.commonpath([full_dir, abs_working_directory]) != abs_working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    elif not os.path.isdir(full_dir):
        return f'Error: "{directory}" is not a directory'

    else:

        file_lst = []

        try:
            items = os.listdir(full_dir)
        except Exception:
            return f'Error: Cannot list "{directory}" - directory does not exist or is inaccessible'

        for item in items:
            try:
                item_path = os.path.join(full_dir, item)
                
                if os.path.isdir(item_path):
                    is_dir = True
                    file_size = os.path.getsize(item_path)
                    file_lst.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

                elif os.path.isfile(item_path):
                    is_dir = False
                    file_size = os.path.getsize(item_path)
                    file_lst.append(f"- {item}: file_size={file_size} bytes, is_dir={is_dir}")

            except Exception:
                continue

        return "\n".join(file_lst)