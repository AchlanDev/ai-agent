
# AI Agent Main Script

import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = "Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"

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
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose_mode:
    print(response.text)
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")

else:
    print(response.text)
#print(messages[0].parts[0].text)