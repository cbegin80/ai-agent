import os

def is_in_working_dir(working_directory, file_path):
    '''
    A function to determine if a file is in the working direcrtory

    parameters:
    working_directory: the current working directory
    file_path: name of a file/directory to check

    Preconditions:
    working_directory and file_path are non-empty strings
    '''
    try:    
        wd_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(wd_abs_path, file_path))
        
        # validate directory path provided
        result = os.path.commonpath([wd_abs_path, file_abs_path]) == wd_abs_path
    except:
        return False
    
    return result