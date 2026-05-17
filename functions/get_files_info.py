import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=("Lists files in a specified directory relative to the working "
    "directory, providing file size and directory status"),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=("Directory path to list files from, relative to "
                             "the working directory (default is the working " \
                             "directory itself)"),
            )
        }
    )
)

def get_files_info(working_directory, directory='.'):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_dir_path = os.path.normpath(os.path.join(wd_abs_path, directory))
        
        # validate directory path provided
        valid_target_dir = os.path.commonpath([wd_abs_path, target_dir_path]) == wd_abs_path

        if not valid_target_dir:
            return(f'Error: Cannot list "{directory}" as it is outisde the permitted working directory')

        if not os.path.isdir(target_dir_path):
            return (f'Error: "{directory}" is not a directory')
        
        # print directory contents
        
        dir_list = os.listdir(target_dir_path)
        output = ""
        for item in dir_list:
            item_path = os.path.normpath(os.path.join(target_dir_path, item))
            item_size = os.path.getsize(item_path)
            
            output +=   (   
                            f"- {item}: file_size={os.path.getsize(item_path)}"
                            f" bytes, is_dir={os.path.isdir(item_path)}\n"
                        )
    except Exception as e:
        output = f"Error: {e}"        
    
    return output
