import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working_directory = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    outside = os.path.commonpath([abs_full_path, abs_working_directory]) != abs_working_directory
    if outside:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'

    files = os.listdir(abs_full_path)

    metadata = []
    for file in os.listdir(full_path):

        file_path = os.path.join(abs_full_path, file)

        size = os.path.getsize(full_path) 

        metadata.append(f"- {file}: file_size={size} bytes, is_dir={os.path.isdir(file_path)}") 
    return f"Result for {directory} directory:\n"+"\n".join(metadata)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, creating it if it does not exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
                
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),   
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

available_functions = [
    types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )
]
