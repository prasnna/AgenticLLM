# Google ADK Agent

This module implements a proof of concept for Google's Agent Development Kit (ADK).

## Overview

The Google ADK Agent demonstrates:
- Creating agents with Google's ADK framework
- Implementing custom function tools
- Using Google's Gemini models
- Running agents locally for testing and development

## Requirements

- Python 3.9+
- Google API key (for Gemini models)
- Google ADK package (`google-adk`)

## Usage

### Running the Agent

You can run the agent using the provided script:

```bash
# Run the agent in interactive mode
python run_google_adk_agent.py
```

### Configuration

You can configure the agent by setting environment variables or editing the `.env` file:

```
# Google ADK configuration
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
GOOGLE_ADK_MODEL_ID=gemini-2.5-pro-preview-03-25
```

## Environment Variables

The agent uses the following environment variables:

- `GOOGLE_API_KEY`: Your Google API key for accessing Gemini models
- `GOOGLE_GENAI_USE_VERTEXAI`: Set to "TRUE" if using Vertex AI (default: "FALSE")
- `GOOGLE_ADK_MODEL_ID`: The Gemini model ID to use (default: "gemini-2.5-pro-preview-03-25")

## Implementation Details

The agent is built using:

- Google ADK for the agent framework
- Google Gemini for the language model
- Custom function tools for specific capabilities

## Features

- Weather information tool (simulated)
- Current time tool

## Project Structure

```
src/agents/google_adk_agent/
├── __init__.py        # Module initialization
├── agent.py           # Agent definition
├── config.py          # Configuration settings
├── .env               # Environment variables
├── README.md          # Documentation
└── tools/             # Function tools
    ├── __init__.py
    └── tools.py       # Tool implementations
```

## Using with ADK CLI

While the recommended way to run the agent is using the provided script, you can also try using the ADK CLI:

```bash
# Run with web UI (experimental)
adk web
```

Note: The ADK CLI integration is still being worked on and may not function correctly.
