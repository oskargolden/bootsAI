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
You are a helpful AI coding agent working with a calculator project.

When a user asks a question or makes a request, you should use the available functions to explore, understand, and modify the codebase as needed. You can perform the following operations:

- List files and directories (use get_files_info)
- Read file contents (use get_file_content) 
- Execute Python files with optional arguments (use run_python_file)
- Write or overwrite files (use write_file)

Always start by exploring the project structure to understand what you're working with. All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Work step by step to fulfill the user's request. When you have completed the task, provide a clear summary of what you did.
"""

def main():
    try: 
        user_prompt = " ".join(sys.argv[1:])
        verbose = "--verbose" in user_prompt
        
        if len(user_prompt.strip()) < 2:
            raise IndexError("No prompt provided")
        
        # Initialize messages with the user prompt
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
        
        # Main agent loop - up to 20 iterations
        for iteration in range(20):
            try:
                # Generate content with the full conversation history
                response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions], 
                        system_instruction=system_prompt
                    ),
                )

                # Handle function calls first - check candidates for function calls
                function_calls_found = False
                for candidate in response.candidates:
                    if candidate.content:
                        # Add candidate content to messages
                        messages.append(candidate.content)
                        
                        # Check for function calls in this candidate
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call:
                                function_calls_found = True
                                function_call = part.function_call
                                
                                # Print the function call - this is what the test expects!
                                print(f" - Calling function: {function_call.name}")
                                
                                function_result = call_function(function_call, verbose=verbose)
                                messages.append(function_result)
                                
                                if verbose and function_result.parts[0].function_response.response:
                                    print(f"-> {function_result.parts[0].function_response.response}")

                # If function calls were found, continue the loop
                if function_calls_found:
                    continue

                # Check if we have a final text response (only if no function calls)
                if response.text:
                    print("Final response:")
                    print(response.text)
                    if verbose:
                        X = response.usage_metadata.prompt_token_count
                        Y = response.usage_metadata.candidates_token_count
                        print(f"\nUser prompt: {user_prompt}")
                        print(f"Prompt tokens: {X}")
                        print(f"Response tokens: {Y}")
                        print(f"Iterations completed: {iteration + 1}")
                    break

                # If no function calls and no text, we're stuck
                print(f"Warning: No text or function call returned in iteration {iteration + 1}")
                break
                    
            except Exception as e:
                print(f"Error in iteration {iteration + 1}: {e}")
                break
        else:
            # Loop completed without breaking (hit max iterations)
            print("Warning: Reached maximum iterations (20) without completion")

    except IndexError:
        print("Please provide a prompt as a command-line argument.")
        print("Example: python main.py 'explain how the calculator works'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()