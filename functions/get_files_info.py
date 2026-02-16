import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
    except:
        raise Exception("Error: working_dir_abs_path couldn't be computed")
    try:
        target_dir_full_path = os.path.normpath(os.path.join(working_dir_abs_path, directory))
    except:
        raise Exception("Error: target_dir_full_path couldn't be computed")
    
    # Will be True or False
    try:
        valid_target_dir = os.path.commonpath([working_dir_abs_path, target_dir_full_path]) == working_dir_abs_path
    except:
        raise Exception("Error: valid_target_dir couldn't be computed")
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir_full_path):
        return f'Error: "{directory}" is not a directory'
    list_of_dir_entries = [
                            os.path.join(target_dir_full_path, a_name)
                            for a_name in os.listdir(target_dir_full_path)
                          ]
    results = ""
    for entry in list_of_dir_entries:
        name = entry
        try:
            file_size = os.path.getsize(name)
        except:
            raise Exception("Error: file_size couldn't be computed")
        try:
            is_dir = os.path.isdir(name)
        except:
            raise Exception("Error: is_dir couldn't be computed")
        results = f"{results}- {os.path.basename(name)}: file_size={file_size} bytes, is_dir={is_dir}\n"
        
    return results
