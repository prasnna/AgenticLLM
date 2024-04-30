# Import necessary modules
import subprocess
import os
from langchain_openai import OpenAI
from config import *
from langchain_core.outputs.generation import Generation

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Set up OpenAI client
openai = OpenAI()


def generate_python_code(prompt: str) -> str:
    """
    Generate Python code for the given prompt using OpenAI's language model.

    Args:
        prompt (str): The prompt for which Python code needs to be generated.

    Returns:
        str: The generated Python code.
    """
    # Generate Python code for the prompt
    response = openai.generate(
        [f"'generate python code alone for the following text', '{prompt}'"]
    )
    op: Generation = response.generations[0][0]
    # Extract the generated code from the response
    python_code = op.text
    return python_code


def generate_python_test_code(code: str) -> str:
    """
    Generate Python unit test code for the given Python code using OpenAI's language model.

    Args:
        code (str): The Python code for which test code needs to be generated.

    Returns:
        str: The generated Python test code with a reference to the original code.
    """
    # Generate Python code for the prompt
    response = openai.generate(
        [f"'generate python unit test code alone for the following code', '{code}'"]
    )
    op: Generation = response.generations[0][0]
    # Extract the generated code from the response
    python_code = op.text
    # Add a reference to the original code
    python_code_with_ref = f"# Original code reference:\n# {code}\n\n{python_code}"
    return python_code_with_ref


def execute_python_code(python_code: str) -> str:
    """
    Execute the given Python code using the subprocess module.

    Args:
        python_code (str): The Python code to be executed.

    Returns:
        str: The output of the executed Python code.
    """
    # Execute the Python code using subprocess
    result = subprocess.check_output(["python", "-c", python_code])
    return result.decode("utf-8").strip()


def generateCodeAndTest(prompt: str) -> str:
    """
    Generate Python code and test code for the given prompt, execute both, and return the output.

    Args:
        prompt (str): The prompt for which Python code and test code need to be generated.

    Returns:
        str: The output of the executed Python code.
    """
    # Generate Python code for the prompt
    python_code = generate_python_code(prompt)
    print(python_code)

    # Generate Python test code for the generated code
    python_test_code = generate_python_test_code(python_code)
    print(python_test_code)

    # Execute the Python code
    result = execute_python_code(python_code)
    print(result)

    # Execute the Python test code
    test_result = execute_python_code(python_test_code)
    print(test_result)

    return result


def main():
    # Get the prompt from the user
    prompt = input("Enter a prompt: ")

    # Generate code and test, execute both, and print the output
    output = generateCodeAndTest(prompt)
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
