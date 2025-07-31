import os

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


