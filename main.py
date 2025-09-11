import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
if len(sys.argv) != 1:
    user_prompt = sys.argv[1]
verbose = "--verbose" in sys.argv

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)

def call_function(function_call_part, is_verbose=False):
    if verbose:
        is_verbose = True
    
    if is_verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    args = function_call_part.args
    args.update({"working_directory": "calculator"})
    
    match function_call_part.name:
        case "get_files_info":
            results = get_files_info(**args)
        case "get_file_content":
            results = get_file_content(**args)
        case "write_file":
            results = write_file(**args)
        case "run_python_file":
            results = run_python_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={"error": f"Unknown function: {function_call_part.name}"},
                    )
                ],
            )
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": results}
            )
        ],
    )

def main():
    if len(sys.argv) == 1:
        raise Exception("prompt not provided")
    for i in range(20):
        try:
            content_response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt),
            )
            for candidate in content_response.candidates:
                messages.append(candidate.content)
            
            if content_response.function_calls:
                for function_call in content_response.function_calls:
                    results = call_function(function_call)
                    if not results.parts[0].function_response.response:
                        raise RuntimeError("Response is somehow missing")
                    messages.append(types.Content(role="user", parts=[types.Part(text=results.parts[0].function_response.response["result"])]))
                    if verbose:
                        print(f'-> {results.parts[0].function_response.response["result"]}')
            else:
                print(content_response.text)
                break
        except Exception:
            break

    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {content_response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {content_response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
