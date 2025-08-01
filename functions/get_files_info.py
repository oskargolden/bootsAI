import os
import subprocess
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified Python file with an optional list of arguments. Must be constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file, constrained to the working directory. Overwrites any existing content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

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

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)



def get_files_info(working_directory, directory='.'):
    #join paths
    current_path = os.path.join(working_directory, directory)

    # get absolute paths for comparison
    abs_working_dir = os.path.abspath(working_directory)
    abs_current_path = os.path.abspath(current_path)
        

    # Check if current_path is outside the working directory
    if not abs_current_path.startswith(abs_working_dir):
       return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    # Check and make sure argument is a directory
    if not os.path.isdir(abs_current_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        # Return string listing contents of the directory
        directory_contents = os.listdir(abs_current_path)

         # Building the formatted strings
        result_lines = []

        for item in directory_contents:
            item_path = os.path.join(abs_current_path, item)
            file_size = os.path.getsize(item_path)
            is_directory = os.path.isdir(item_path)
            
            line = f"- {item}: file_size={file_size} bytes, is_dir={is_directory}"
            result_lines.append(line)
        
        return "\n".join(result_lines)




    except Exception as e:
        return f'Error: {str(e)}'

def get_file_content(working_directory, file_path):

    # get absolute paths for comparison

    # Step 1: Combine the working directory and the relative file path
    # Example: "calculator" + "lorem.txt" becomes "calculator/lorem.txt"
    combined_path = os.path.join(working_directory, file_path)

    # Step 2: Get the absolute path of this combined path
    # Example: "calculator/lorem.txt" becomes "/full/path/to/project/calculator/lorem.txt"
    abs_current_path = os.path.abspath(combined_path)


    # abs path of target directory 
    abs_working_dir = os.path.abspath(working_directory)

    # Check if the file_path is outside the working_directory
    if not abs_current_path.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    # Check and make sure argument is a file
    if not os.path.isfile(abs_current_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    

    try:
        # Return string, listing contents of the file
        #file_content_string = os.listdir(abs_current_path)

        MAX_CHARS = 10000

        with open(abs_current_path, "r") as f:
            file_string = f.read(MAX_CHARS + 1)
        
            
        if len(file_string) > MAX_CHARS:
            file_string = file_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at 10000 characters]'
                 
            return file_string    
        else:

            return file_string

    except Exception as e:
        return f'Error: {str(e)}'
   
def write_file(working_directory, file_path, content):
    """
    Writes content to a file, ensuring the file path is within the specified working directory.
    If the directory for the file does not exist, it will be created.

    Args:
        working_directory (str): The root directory where files are allowed to be written.
        file_path (str): The relative path to the file from the working_directory.
        content (str): The string content to write to the file.

    Returns:
        str: A success message if the write is successful, or an error message otherwise.
    """
    # Create the full, combined path to the target file.
    full_path = os.path.join(working_directory, file_path)
    
    # Get the absolute, canonical paths of the working directory and the full file path.
    # This is a security measure to prevent writing to a file outside the working_directory
    # using path traversal techniques (e.g., "../").
    abs_working_dir = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    # Check if the absolute path of the file to be written starts with the absolute
    # path of the working directory. If it doesn't, it's an invalid path.
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        # Get the directory part of the full file path.
        dir_name = os.path.dirname(full_path)
        
        # Create the directory and all parent directories if they don't exist.
        # The exist_ok=True argument prevents an error if the directory already exists.
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
                
        # Open the file in write mode ("w") which will create the file if it doesn't
        # exist or overwrite its contents if it does.
        with open(full_path, "w") as f:
            f.write(content)
    
        # Return a success message with the number of characters written.
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        # Catch any potential errors during the process and return an error message.
        return f'Error: {str(e)}'

def run_python_file(working_directory, file_path, args=None):
    
    """
    FUNCTION"

    This allows ai agent to execute python code. It ensures the file path is within the specified working directory.
    If the directory for the file does not exist, or if not with in correct directory, code will not attempt to execute.

    Args:
        working_directory (str): The root directory where files are allowed to be written.
        file_path (str): The relative path to the file from the working_directory.
        args (list): A list of additional command-line arguments to pass to the script.
        

    Returns:
        str: A success message if the execution is successful, or an error message otherwise.
    """
    if args is None:
        args = []

    # Get absolute paths for security checks
    abs_working_dir = os.path.abspath(working_directory)
    full_path = os.path.join(abs_working_dir, file_path)
    abs_full_path = os.path.abspath(full_path)

    # Security check: Ensure the file is within the working directory
    if not abs_full_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    # Check if the file exists
    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if it's a Python file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'

    # Construct the command to run
    command = ['python', abs_full_path] + args
    
    # Execute Python file 
    try:
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,  # Decode stdout and stderr as text
            timeout=30,
            check=True  # Raise an exception if the command returns a non-zero exit code
        )
        
        # If execution is successful and `check=True` is not triggered
        return f'Execution successful.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}'
        
    except subprocess.CalledProcessError as e:
        return f'Error: The Python script returned a non-zero exit code.\nReturn code: {e.returncode}\nStdout:\n{e.stdout}\nStderr:\n{e.stderr}'
    except subprocess.TimeoutExpired:
        return f'Error: The Python script timed out after 30 seconds.'
    except FileNotFoundError:
        return f'Error: The "python" command was not found. Please ensure Python is installed and in your system\'s PATH.'
    except Exception as e:
        return f'Big Bad Errorrr: {e}'
    
def call_function(function_call_part, verbose=False):
    """
    Calls a specified function based on the LLM's function call part.
    
    Args:
        function_call_part (types.FunctionCall): The function call object from the LLM.
        verbose (bool): If True, prints verbose output.
        
    Returns:
        types.Content: A Content object containing the function's result or an error.
    """
    function_name = function_call_part.name
    function_args = dict(function_call_part.args)
    
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Manually add the working directory for security
    function_args["working_directory"] = "./calculator"

    try:
        # Call the function using the dictionary of keyword arguments.
        function_result = function_map[function_name](**function_args)
        
        # Return the result in the required format.
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Error executing function: {e}"},
                )
            ],
        )
        
        
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}