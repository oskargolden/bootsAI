import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)



def main():
    try: 
        user_prompt = " ".join(sys.argv[1:])
        messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
        if len(user_prompt) < 2:
            raise IndexError("No prompt provided")
        if "--verbose" in user_prompt:
            response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)
            X = response.usage_metadata.prompt_token_count
            Y = response.usage_metadata.candidates_token_count
            print("User prompt:", user_prompt)
            print("Prompt tokens:", X)
            print("Response tokens:", Y)
            print(response.text) 
            
        response = client.models.generate_content(model="gemini-2.0-flash-001",contents=messages,)    
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