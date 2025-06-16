import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = (
            os.path.abspath(file_path)
            if os.path.isabs(file_path)
            else os.path.abspath(os.path.join(abs_working_directory, file_path))
        )
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        parent_dir = os.path.dirname(abs_file_path)
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)
        with open(abs_file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {str(e)}'
