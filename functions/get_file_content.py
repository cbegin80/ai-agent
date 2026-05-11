import os
from functions.utils import is_in_working_dir

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    try:
        # if file_path is not in the working directory
        if not is_in_working_dir(working_directory, file_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        full_file_path = os.path.join(working_directory, file_path)
        # if file_path is not a file
        if not os.path.isfile(full_file_path):
            # return error string
            return (f'Error: File not found or is not a regular file:'
                    f'"{file_path}"')

        # open file
        with open(full_file_path, 'r') as f:
            # convert file contents to string (up to 10000 chars)
            file_content = f.read(10000)
        # if file is longer than 10k chars
            if f.read(1):
                #add file_size message
                file_content += (f'[...File "{file_path}" truncated at '
                                 f'{MAX_CHARS} characters]')
        
        return file_content
    
    except Exception as e:
        return f"Error: {e}"