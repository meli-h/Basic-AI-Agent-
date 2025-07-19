import os 
from dotenv import load_dotenv
from google import genai
import sys 
from google.genai import types
import argparse
from functions.get_files_info import available_functions
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

load_dotenv()   
api_key = os.environ.get("GEMINI_API_KEY")


function_mapping = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,   
    "write_file": write_file,               
    "run_python_file": run_python_file,     
}


client = genai.Client(api_key=api_key)
system_prompt = """
You are a helpful AI agent designed to help the user write code within their codebase.

When a user asks a question or makes a request, make a function call plan. For example, if the user asks "what is in the config file in my current directory?", your plan might be:

1. Call a function to list the contents of the working directory.
2. Locate a file that looks like a config file
3. Call a function to read the contents of the config file.
4. Respond with a message containing the contents

You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security.

You are called in a loop, so you'll be able to execute more and more function calls with each message, so just take the next step in your overall plan.

Most of your plans should start by scanning the working directory (`.`) for relevant files and directories. Don't ask me where the code is, go look for it with your list tool.

Execute code (both the tests and the application itself, the tests alone aren't enough) when you're done making modifications to ensure that everything works as expected.
"""
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()
    
    if args.verbose:
        print(f"User prompt: {args.prompt}")

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)]),
    ]

    for step in range(20):          
        try:                       
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,            
                config=types.GenerateContentConfig(
                    tools=available_functions,
                    system_instruction=system_prompt,
                ),
            )
        except Exception as exc:
            print(" LLM error:", exc)         
            break

        if response.candidates:
            for _ in  response.candidates:
                messages.append(_.content)
        
        

        if response.function_calls:

            tool_msg = call_function(
            response.function_calls[0],
            verbose=args.verbose
            )
            messages.append(tool_msg)
            if args.verbose:
                print(f'→ {resp_dict["result"]}')
        else:
            print(f"Final response: \n {response.text}")
            break
    

    
        
    
    
        
    
def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    if function_call_part.name not in function_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    python_func = function_mapping[function_call_part.name]
    kwargs = dict(function_call_part.args)
    kwargs["working_directory"] = "./calculator"

    result = python_func(**kwargs)

    
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )

    
    

if __name__ == "__main__":
    main()
