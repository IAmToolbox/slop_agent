import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if working_directory not in abs_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_path):
        with open(abs_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    else:
        with open(abs_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to the specified file path. If the file doesn't exist, the function creates a new file. Otherwise, it overwrites the contents of the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file to be written.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written into the file."
            ),
        },
    ),
)