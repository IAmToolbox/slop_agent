import os

MAX_CHARACTERS = 10000

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    if working_directory not in abs_path:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_path) or not os.path.exists(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    with open(abs_path, "r") as f:
        file_content = f.read(MAX_CHARACTERS)
        if len(file_content) == MAX_CHARACTERS:
            file_content = f'{file_content}[...File "{file_path}" truncated at {MAX_CHARACTERS} characters]'
        return file_content
    
