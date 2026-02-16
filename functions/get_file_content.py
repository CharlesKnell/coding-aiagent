from config import MAX_CHARS
import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists the content of a file within a specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
    except:
        raise Exception("Error: working_dir_abs_path couldn't be computed")
    try:
        target_file_full_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    except:
        raise Exception("Error: target_file_full_path couldn't be computed")
    
    # Will be True or False
    try:
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_full_path]) == working_dir_abs_path
    except:
        raise Exception("Error: valid_target_file couldn't be computed")
    if not valid_target_file:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    with open(target_file_full_path, "r", encoding="utf-8") as f:
        content = f.read(MAX_CHARS)
        if f.read(1):
            content += f'[...File "{target_file_full_path}" truncated at {MAX_CHARS} characters]'
    return content
    