import subprocess

def run_bandit(path):
    """
    Run Bandit for static code analysis.

    Args:
        path (str): Path to the directory or file to be analyzed.
    """
    print("Running Bandit for static code analysis...")
    try:
        subprocess.run(["bandit", "-r", path], check=True)
        print("Bandit analysis completed without finding any issues.")
    except subprocess.CalledProcessError:
        print("Bandit found security issues in the code.")

def run_safety():
    """
    Run Safety for dependency scanning.
    """
    print("Running Safety for dependency scanning...")
    try:
        subprocess.run(["safety", "check", "--full-report"], check=True)
        print("Safety scan completed without finding any issues.")
    except subprocess.CalledProcessError:
        print("Safety found security vulnerabilities in dependencies.")

if __name__ == "__main__":
    # Specify the path to the directory or file to be analyzed
    code_path = "C:/Users/pparthasarathy/Desktop/AgenticLLM/AgenticLLM/scripts"

    # Perform static code analysis with Bandit
    run_bandit(code_path)

    # Perform dependency scanning with Safety
    run_safety()
