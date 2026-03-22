import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="It goes to the given file path, and checks if it a python file. If it is, then it execute it, returning an output string that contains STDOUT and STDERR, also gives error when nessecery",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="It is the file path that will be taken inside the given working directory, validity will be checked by the function"
            ),
            "args": types.Schema(
                type = types.Type.ARRAY,
                description="It is a list that contains any nessecery argument to run the python file",
                items = types.Schema(
                    type=types.Type.STRING,
                    description="Argument as string"
                )
            )
        },
        required=["file_path"]
    )
)

def run_python_file(working_directory, file_path, args=None):
    # try:

        absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(absolute_path, file_path))

        valid_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

        if not valid_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_dir.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'


        command = ["python", target_dir]

        if args is not None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=os.path.dirname(target_dir), capture_output=True, text=True, timeout=30)

        output_string = ""

        if completed_process.returncode != 0:
            output_string += f'Process exited with code {completed_process.returncode}\n'

        if completed_process.stdout:
            output_string += f'STDOUT: {completed_process.stdout}'
        
        if completed_process.stderr:
            output_string += f'\nSTDERR: {completed_process.stderr}'

        if not completed_process.stdout and not completed_process.stderr:
            output_string += "No output produced"

        return output_string
    
    # except Exception as e:

    #     return f'Error: executing Python file: {e}'

