import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

from functions.call_function import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def load_client():
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)
	return client

def verbose_print(user_prompt, response):
	print(f"User prompt: {user_prompt}")
	print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
	print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def main():
				# get arguments from command line
				# If there is --verbose flag, print verbose information
				if "--verbose" in sys.argv:
								sys.argv.remove("--verbose")
								verbose = True
				else:
								verbose = False

				user_prompt = sys.argv[1:]
				if len(user_prompt) == 0:
								print("Please provide a prompt as an argument.")
								sys.exit(1)

				client = load_client()

				messages = [
								types.Content(role="user", parts=[types.Part(text=user_prompt[0])]),
				]

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
				schema_get_file_content = types.FunctionDeclaration(
								name="get_file_content",
								description="Get the content of files in the specified directory, constrained to the working directory.",
								parameters=types.Schema(
												type=types.Type.OBJECT,
												properties={
																"file_path": types.Schema(
																				type=types.Type.STRING,
																				description="The path to the file to get content from, relative to the working directory.",
																),
												},
								),
				)
				schema_run_python_file = types.FunctionDeclaration(
								name="run_python_file",
								description="Run a Python file in the specified directory, constrained to the working directory.",
								parameters=types.Schema(
												type=types.Type.OBJECT,
												properties={
																"file_path": types.Schema(
																				type=types.Type.STRING,
																				description="The path to the file to get content from, relative to the working directory.",
																),
												},
								),
				)
				schema_write_file = types.FunctionDeclaration(
								name="write_file",
								description="Write content to a file in the specified directory, constrained to the working directory.",
								parameters=types.Schema(
												type=types.Type.OBJECT,
												properties={
																"file_path": types.Schema(
																				type=types.Type.STRING,
																				description="The path to the file to get content from, relative to the working directory.",
																),
																"content": types.Schema(
																				type=types.Type.STRING,
																				description="The content to write to the file.",
																),
												},
								),
				)

				available_functions = types.Tool(
								function_declarations=[
												schema_get_files_info,
												schema_get_file_content,
												schema_write_file,
												schema_run_python_file,
								]
				)

				max_iterations = 20
				for _ in range(max_iterations):
								response = client.models.generate_content(
												model="gemini-2.0-flash-001",
												contents=messages,
												config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
								)
								# Add all candidate contents to messages
								if hasattr(response, "candidates") and response.candidates is not None:
												for candidate in response.candidates:
																if hasattr(candidate, "content") and candidate.content is not None:
																				messages.append(candidate.content)

								if hasattr(response, "function_calls") and response.function_calls:
												for function_call in response.function_calls:
																function_call_result = call_function(function_call, verbose=verbose)
																# Append the function result to messages
																if function_call_result is not None:
																				messages.append(function_call_result)
																				# Optionally print result if verbose
																				if verbose:
																								try:
																												result = function_call_result.parts[0].function_response.response
																												print(f"-> {result}")
																								except (AttributeError, IndexError, TypeError):
																												print("Function call did not return a valid response.")
												# Continue to next iteration
								else:
												print("Final response:")
												print(getattr(response, "text", "No response text available."))
												if verbose:
																verbose_print(user_prompt[0], response)
												break
				else:
								print("Max iterations reached. Exiting.")


main()
