from google.genai import types
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file

def call_function(function_call_part, verbose=False):
	function_name = function_call_part.name
	args = dict(function_call_part.args)
	args["working_directory"] = "./calculator"

	if verbose:
		print(f"Calling function: {function_name}({function_call_part.args})")
	else:
		print(f" - Calling function: {function_name}")

	function_dict = {
		"get_files_info": get_files_info,
		"get_file_content": get_file_content,
		"run_python_file": run_python_file,
		"write_file": write_file,
	}

	func = function_dict.get(function_name)
	if func is None:
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=function_name,
					response={"error": f"Unknown function: {function_name}"},
				)
			],
		)

	try:
		function_result = func(**args)
	except Exception as e:
		function_result = f"Exception during function call: {e}"

	return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
