from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file as get_file_write
from functions.run_python import run_python_file

import time

cases_for_info = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

cases_for_content = [
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exist.py"),
]

cases_for_write = [
    ("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


# for name, path, content in cases_for_write:
#     result = get_file_write(name, path, content)
#     print(result)
#     if (name, path) != cases_for_content[-1]:     
#         time.sleep(2)

funcs = [run_python_file("calculator", "main.py"),
    run_python_file("calculator", "main.py", ["3 + 5"]), 
    run_python_file("calculator", "tests.py"),
    run_python_file("calculator", "../main.py"), 
    run_python_file("calculator", "nonexistent.py")]

for func in funcs:
    result = func
    print(result)
        
    time.sleep(2)
    
    
