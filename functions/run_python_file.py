import os, subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a file within a specified working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of argument strings",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
    except:
        raise Exception("Error: working_dir_abs_path couldn't be computed")
    try:
        target_file_full_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
    except:
        raise Exception("Error: target_file_full_path couldn't be computed")
    try:
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs_path, target_file_full_path]) == working_dir_abs_path
    except:
        raise Exception("Error: valid_target_file couldn't be computed")
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_file_full_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not target_file_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    try:
        command = ["python3", target_file_full_path]
        if args:
            command.extend(args)

        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        out_string = ""
        if completed_process.returncode != 0:
            out_string += f"Process exited with code {completed_process.returncode}\n"

        stderr_text = completed_process.stderr.strip()
        stdout_text = completed_process.stdout.strip()

        if not stdout_text and not stderr_text:
            out_string += "No output produced\n"
        else:
            if stdout_text:
                out_string += "STDOUT:\n" + completed_process.stdout + "\n"             
            if stderr_text:
                out_string += "STDERR:\n" + completed_process.stderr + "\n"      
    except Exception as e:
        raise Exception(f"Error: executing Python file: {e}")
    return out_string
