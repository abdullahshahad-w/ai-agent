import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="It goes to the given file path, and then writes the given content in the file within the restricted working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="It is the file path that will be taken inside the given working directory, validity will be checked by the function"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="It the argument taken as a string and then written in the file given by the file path"
            )
        },
        required=["file_path", "content"]
    )
)

def write_file(working_directory, file_path, content):

    try:
        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

        valid_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_dir):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent = os.path.dirname(target_dir)

        if parent:
            os.makedirs(parent, exist_ok=True)

        with open(target_dir, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {e}'