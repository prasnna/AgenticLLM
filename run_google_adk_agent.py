#!/usr/bin/env python3
"""
Run script for the Google ADK agent.
"""

import os
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import our agent
from src.agents.google_adk_agent.agent import root_agent

def main():
    """
    Run the Google ADK agent.
    """
    # Load environment variables
    load_dotenv()
    
    print("Initializing Google ADK Agent...")
    
    # Check if API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("\nWarning: GOOGLE_API_KEY environment variable not set.")
        print("You can set it in the .env file or in your environment variables.")
        print("Without an API key, the agent will not be able to use Gemini models.")
        print("Continuing with demo mode (simulated responses)...\n")
    
    # Set up session service and runner
    app_name = "google_adk_demo"
    user_id = "user123"
    session_id = "session123"
    session_service = InMemorySessionService()
    session = session_service.create_session(
        app_name=app_name, 
        user_id=user_id, 
        session_id=session_id
    )
    runner = Runner(
        agent=root_agent, 
        app_name=app_name, 
        session_service=session_service
    )
    
    # Run interactive loop
    print("Google ADK Agent initialized. Type 'exit' to quit.")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        content = types.Content(role='user', parts=[types.Part(text=query)])
        events = runner.run(
            user_id=user_id, 
            session_id=session_id, 
            new_message=content
        )
        
        for event in events:
            if event.is_final_response():
                final_response = event.content.parts[0].text
                print(f"\nAgent: {final_response}")

if __name__ == "__main__":
    main()
