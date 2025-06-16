import os

def get_files_info(working_directory, directory=None):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        if directory is None:
            abs_directory = abs_working_directory
        else:
            # If directory is absolute, use as is; if relative, resolve relative to working_directory
            abs_directory = (
                os.path.abspath(directory)
                if os.path.isabs(directory)
                else os.path.abspath(os.path.join(abs_working_directory, directory))
            )
        if not abs_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(abs_directory):
            return f'Error: "{directory}" is not a directory'
        entries = []
        for entry in os.listdir(abs_directory):
            entry_path = os.path.join(abs_directory, entry)
            try:
                file_size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                entries.append(f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}')
            except Exception as e:
                entries.append(f'- {entry}: Error: {str(e)}')
        return '\n'.join(entries)
    except Exception as e:
        return f'Error: {str(e)}'
