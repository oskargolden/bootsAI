import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import *
load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, you MUST make a function call to fulfill their request. You can perform the following operations:

- List files and directories (use get_files_info)
- Read file contents (use get_file_content) 
- Execute Python files with optional arguments (use run_python_file)
- Write or overwrite files (use write_file)

ALWAYS use function calls rather than just responding with text. All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

If a user asks to read a file, get file contents, or view a file, use the get_file_content function.
"""

def main():
    try: 
        user_prompt = " ".join(sys.argv[1:])
        verbose = "--verbose" in user_prompt
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
        if len(user_prompt) < 2:
            raise IndexError("No prompt provided")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
        )

        if response.function_calls:
            function_call_part = response.function_calls[0]
            
            # Call the new function to execute the LLM's plan
            function_call_result = call_function(function_call_part, verbose=verbose)
            
            if verbose:
                # Print the result of the function call
                if function_call_result.parts[0].function_response.response:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                else:
                    raise Exception("Function call result has no response.")
            
        else:
            if verbose:
                X = response.usage_metadata.prompt_token_count
                Y = response.usage_metadata.candidates_token_count
                print("User prompt:", user_prompt)
                print("Prompt tokens:", X)
                print("Response tokens:", Y)
            print(response.text)
        
        print("Hello from bootsai!")
    except IndexError:
        print("Please provide a prompt as a command-line argument.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()