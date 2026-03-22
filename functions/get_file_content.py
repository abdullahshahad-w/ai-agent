import os
from config import MAX_CHARS_TO_READ
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="It reads the content of the specified file, and returns it as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="It is the file path that will be taken inside the given working directory, validity will be checked by the function"

            )
        },
        required=["file_path"]
    )
)

def get_file_content(working_directory, file_path):
    absolute_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_dir, file_path))

    # if not os.path.isdir(target_dir):
    #     return f'Error: "{target_dir}" is not a directory'

    valid_dir  = os.path.commonpath([absolute_dir, target_dir]) == absolute_dir

    if not valid_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_dir):
        return f'Error: File not found or it is not a regular file: "{file_path}"'

    with open(target_dir) as f:
        file_content_string = f.read(MAX_CHARS_TO_READ)

        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'

        return file_content_string

