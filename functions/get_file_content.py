import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = (
            os.path.abspath(file_path)
            if os.path.isabs(file_path)
            else os.path.abspath(os.path.join(abs_working_directory, file_path))
        )
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(abs_file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        if len(content) > MAX_CHARS:
            return content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at 10000 characters]'
        return content
    except Exception as e:
        return f'Error: {str(e)}'
