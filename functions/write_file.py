import os
from functions.utils import is_in_working_dir
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=("Writes a Python file in the working directory.\n"
                 "If the file already exists, it is overwritten."),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=("Path to the file to write, relative to "
                             "the working directory (default is the working " \
                             "directory itself)."),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description=("The content to write to the file.")          
            )
        },
        required=["file_path"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        #ensure file_path is in the working directoy
        if not is_in_working_dir(working_directory, file_path):
            return (f'Error: Cannot write to "{file_path}" as it is outside the '
                    f'permitted working directory')
        
        full_file_path = os.path.join(working_directory, file_path)

        # make sure file name is not a directory
        if os.path.isdir(full_file_path):
            return (f'Error: Cannot write to "{file_path}" as it is a directory')
        
        # build file path if it does not exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        with open(full_file_path, 'w') as f:
            f.write(content)
    
        return (f'Successfully wrote to "{file_path}" ({len(content)} '
                f'characters written)')
    except Exception as e:    
        return f'Error: {e}'