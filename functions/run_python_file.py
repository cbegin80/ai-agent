import os
import subprocess
from functions.utils import is_in_working_dir

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