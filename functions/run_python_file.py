import os
import subprocess
from functions.utils import is_in_working_dir
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=("Runs a Python file in the working directory."),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=("Path to the file to access, relative to "
                             "the working directory (default is the working " \
                             "directory itself)."),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="A list of arguments to run with the file command."
                )          
            )
        },
        required=["file_path"]
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:    
        if not is_in_working_dir(working_directory, file_path):
            return (f'Error: Cannot execute "{file_path}" as it is outside the '
                    f'permitted working directory')
        
        full_file_path = os.path.join(working_directory, file_path)

        if not os.path.isfile(full_file_path):
            return (f'Error: "{file_path}" does not exist or is not '
                    f'a regular file')
        
        if not full_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        # build subprocess command
        command = ["python3", file_path]
        if args:
            command.extend(args)

        subprocess_result = subprocess.run(command, cwd=working_directory,
                                        capture_output=True, text=True, 
                                        timeout=30)
        
        result = ""
        if subprocess_result.returncode != 0:
            result = f"Process exited with code {subprocess_result.returncode}"
        if subprocess_result.stdout == None and subprocess_result.stderr == None:
            result += "\nNo output produced"
        else:
            if subprocess_result.stdout:
                result += f"\nSTDOUT: {subprocess_result.stdout}"
            if subprocess_result.stderr:
                result += f"\nSTDERR: {subprocess_result.stderr}"

        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"