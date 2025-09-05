import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if working_directory not in abs_path:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
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

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file, with optional argument declaration.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python file to be executed.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="The arguments that will be passed to the executed file, given as a list of strings. If not provided, an empty list is passed instead.",
                items=types.Schema(
                    type=types.Type.STRING
                ),
            ),
        },
    ),
)