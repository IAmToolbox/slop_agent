import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if working_directory not in abs_path:
        return f'Error: Cannot execute to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'
    
    total_arguments = ["uv", "run", os.path.join(working_directory, file_path)]
    if len(args) > 0:
        total_arguments.extend(args)
    try:
        result = subprocess.run(total_arguments, capture_output=True, text=True, timeout=30)
        result_string = f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"
        if result.returncode != 0:
            result_string += f"\nProcess exited with code {result.returncode}"
        if len(result.stdout) == 0:
            return "No output produced."
        return result_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
