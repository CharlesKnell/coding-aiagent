import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file within a specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path","content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to be written into file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
    except:
        raise Exception("Error: working_dir_abs_path couldn't be computed")
    try:
        target_file_full_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    except:
        raise Exception("Error: target_file_full_path couldn't be computed")
    
    try:
        os.makedirs(os.path.dirname(target_file_full_path), exist_ok=True)
    except:
        raise Exception("Error: makedirs failed")

    if os.path.isdir(target_file_full_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_full_path]) == working_dir_abs_path
    except:
        raise Exception("Error: valid_target_file couldn't be computed")
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    


    try:
        with open(target_file_full_path, "w", encoding="utf-8") as f:
            f.write(content)
    except:
        raise Exception(f"Error: write to {target_file_full_path} failed")

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'