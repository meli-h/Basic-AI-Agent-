import os
import subprocess
def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_full_path = os.path.abspath(full_path)
    abs_working_directory = os.path.abspath(working_directory)
    outside = os.path.commonpath([abs_full_path, abs_working_directory]) != abs_working_directory
    if outside:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    

    a = subprocess.run(['python', abs_full_path] + args, cwd=abs_working_directory, timeout=30, capture_output=True)
    if a.returncode != 0:
        return f'Error: Process exited with code {a.returncode}'
    if a.stdout:
        return f"STDOUT: {a.stdout}"
    elif a.stderr:
        return f'STDERR: {a.stderr}'
    else:
        return 'No output produced.'
        




