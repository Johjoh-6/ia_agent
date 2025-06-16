import os
import subprocess

def run_python_file(working_directory, file_path):
    try:
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = (
            os.path.abspath(file_path)
            if os.path.isabs(file_path)
            else os.path.abspath(os.path.join(abs_working_directory, file_path))
        )
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python", abs_file_path],
                capture_output=True,
                text=True,
                cwd=abs_working_directory,
                timeout=30
            )
            output = []
            output.append(f"STDOUT:\n{result.stdout.strip()}" if result.stdout.strip() else "STDOUT:\n")
            output.append(f"STDERR:\n{result.stderr.strip()}" if result.stderr.strip() else "STDERR:\n")
            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")
            if not result.stdout.strip() and not result.stderr.strip():
                return "No output produced."
            return "\n".join(output)
        except Exception as e:
            return f"Error: executing Python file: {e}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
