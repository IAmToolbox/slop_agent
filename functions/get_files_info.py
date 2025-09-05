import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    #print(path)
    if working_directory not in os.path.abspath(path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    
    contents_list = os.listdir(path)
    info_strings = []
    if directory == ".":
        info_strings.append("Result for current directory:")
    else:
        info_strings.append(f"Result for '{directory}' directory")
    
    for object in contents_list:
        abs_object = os.path.join(path, object)
        info_strings.append(f'- {object}: file_size={os.path.getsize(abs_object)} bytes, is_dir={os.path.isdir(abs_object)}')
    
    return "\n".join(info_strings)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory alo0ng with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)