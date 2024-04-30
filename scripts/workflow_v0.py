
import subprocess
import os
from langchain import OpenAI

import os

# Set OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "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"

#import subprocess
import os
from langchain_openai import OpenAI

# Set up OpenAI client
openai = OpenAI()

def solve_math_prompts(prompt: str) -> str:
    # Use OpenAI to generate a task from the prompt
    response = openai.generate(['I want to add 2 & 8,generate input to calculator as text'])

    print(response)

    # Extract the math problem from the response
    math_problem = response["choices"][0]["text"]

    # Use subprocess to run calc.exe and get the result
    result = subprocess.check_output(f"calc.exe {math_problem}", shell=True)

    return result.decode("utf-8").strip()

# Test the function
prompt = "What is 2 + 2?"
print(solve_math_prompts(prompt))  # Output: 4

#https://chat.openai.com/share/08917362-fee0-4443-847b-fb7048344fb7
