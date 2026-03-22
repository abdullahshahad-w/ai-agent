import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)"
            )
        }
    )
)

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, directory))

    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'

    valid_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if not valid_dir:
        return f'Result for "{directory}":\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'

    directory_list = os.listdir(target_dir)

    ls_info = []
    for element in directory_list:
        path = os.path.join(target_dir, element)
        ls_info.append(f"{element}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")

    items = "\n - ".join(ls_info)

    if directory == ".":
        return f"Result for current directory:\n - {items}"
    else:
        return f"Result for '{directory}':\n - {items}"

    
