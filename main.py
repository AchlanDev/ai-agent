
# AI Agent Main Script

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan.
When asked to do something, do it directly without asking for permission.
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
    description="Reads the content of a specified file up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read file from, relative to the working directory. If not provided, return the error or exception that was caused."
            )
        }
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a python file in the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the python script to execute, relative to the working directory. If not provided, return the error or exception that was caused."
            )
        }
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the given content to a file, creating any necessary directories, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to write to, relative to the working directory. If not provided, return the error or exception that was caused."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text data to be written into the target file. If not provided, return the error or exception that was caused."
            )
        }
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

# Load environment variables from .env file
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if len(sys.argv) < 2:
    print("Prompt not provided.")
    sys.exit(1)

user_prompt = sys.argv[1]
verbose_mode = "--verbose" in sys.argv

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose_mode:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

if response.function_calls:
    for function in response.function_calls:
        function_call_result = call_function(function, verbose=verbose_mode)
        if (
            not function_call_result.parts
            or not hasattr(function_call_result.parts[0], "function_response") 
            or not hasattr(function_call_result.parts[0].function_response, "response")
        ):
            raise Exception("Fatal Exception: cannot continue.")
        if verbose_mode:
            print(f"-> {function_call_result.parts[0].function_response.response}")

else:
    print(response.text)