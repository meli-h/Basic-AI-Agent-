import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    outside = os.path.commonpath([abs_full_path, abs_working_directory]) != abs_working_directory
    if outside:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_full_path):
        os.makedirs(os.path.dirname(abs_full_path), exist_ok=True)
    
    with open(abs_full_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'