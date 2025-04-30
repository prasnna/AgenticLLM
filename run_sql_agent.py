"""
Wrapper script to run the SQL agent with the correct Python path

This script addresses the following issues:
1. Fixes the ModuleNotFoundError for 'src' by adding the project root to the Python path
2. Provides instructions for fixing LangChain deprecation warnings
3. Handles database connection issues gracefully

Usage:
    python run_sql_agent.py [query]

    If a query is provided as a command-line argument, it will be used as input to the SQL agent.
    Otherwise, the default query from the script will be used.

Requirements:
    - Install the required packages:
      pip install langchain-huggingface
"""
import os
import sys
import warnings
import time

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Add the project root directory to the Python path
# This allows absolute imports starting with 'src' to work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    try:
        # Import necessary modules
        from src.utils.env_utils import load_env_vars, get_env_var

        # Load environment variables
        load_env_vars()

        # Check if database URL is set
        db_url = get_env_var("DB_URL")
        if not db_url:
            url = get_env_var("URL")
            if not url:
                print("\nError: Database URL not found in environment variables.")
                print("Please set either DB_URL or URL in your .env file.")
                sys.exit(1)
            db_url = f"mssql+pyodbc://{url}?driver=SQL+Server+Native+Client+10.0"

        # Check if AWS profile is set for Bedrock
        aws_profile = get_env_var("BED_ROCK_AWS_PROFILE")
        if not aws_profile:
            print("\nWarning: BED_ROCK_AWS_PROFILE not set in environment variables.")
            print("Using default value 'saml'.")

        # Check if OpenAI API key is set
        openai_api_key = get_env_var("OPENAI_API_KEY")
        if not openai_api_key:
            print("\nWarning: OPENAI_API_KEY not set in environment variables.")

        # Import the agent executor with a timeout
        print("\nInitializing SQL agent...")
        try:
            # Set a timeout for importing the module
            import threading
            import importlib

            def import_with_timeout():
                global agent_executor
                from src.agents.sql_agent.conversewithSQL_bed_rock_private import agent_executor

            import_thread = threading.Thread(target=import_with_timeout)
            import_thread.daemon = True
            import_thread.start()

            # Wait for the import to complete with a timeout
            import_thread.join(timeout=30)

            if import_thread.is_alive():
                print("\nWarning: Import is taking longer than expected.")
                print("This might be due to database connection issues.")
                print("Press Ctrl+C to cancel or wait for it to complete.")

            # Wait for the import to complete
            while import_thread.is_alive():
                time.sleep(1)

            # Get the agent_executor from the module
            from src.agents.sql_agent.conversewithSQL_bed_rock_private import agent_executor

            # Get query from command line arguments or use default
            query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "find how many agents are there with an email address of donotsend@prac.com"

            print(f"\nExecuting query: {query}")
            result = agent_executor.invoke(input=query)

            print("\nSQL Agent executed successfully.")
            print("\nResult:")
            print(result.get('output', 'No output returned'))

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\nError executing SQL agent: {e}")
            sys.exit(1)

    except ImportError as e:
        print(f"\nError: {e}")
        print("\nYou may need to install additional packages:")
        print("  pip install langchain-huggingface")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
