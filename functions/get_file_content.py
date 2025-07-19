import os 

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    outside = os.path.commonpath([abs_full_path, abs_working_directory]) != abs_working_directory
    if outside:
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_full_path):
        return f'Error: File not found or is not a regular file: "{abs_full_path}"' 

    

    with open(abs_full_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)

    return f'{file_content_string}[File "{file_path}" truncated at 10000 characters]'