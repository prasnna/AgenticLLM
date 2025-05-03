"""
Custom memory extraction utilities for AWS Bedrock models.

This module provides functions to extract structured memories from conversations
without relying on function calling, which may not be supported by all models.
"""

import json
import uuid
from typing import Dict, List, Any, Type, Optional

from langchain_aws import ChatBedrockConverse
from pydantic import BaseModel, ValidationError

def extract_memories(
    llm: ChatBedrockConverse,
    messages: List[Dict[str, str]],
    schema_class: Type[BaseModel],
    instructions: str,
    existing_memories: Optional[List[Dict[str, Any]]] = None
) -> List[Dict[str, Any]]:
    """
    Extract structured memories from a conversation using a structured prompt.

    Args:
        llm: The language model to use for extraction
        messages: The conversation messages
        schema_class: The Pydantic model class defining the memory structure
        instructions: Instructions for memory extraction
        existing_memories: Optional list of existing memories to consider

    Returns:
        A list of extracted memories as dictionaries
    """
    # Create a schema description from the Pydantic model
    schema_fields = []
    model_schema = schema_class.model_json_schema()

    for field_name, field_info in model_schema.get("properties", {}).items():
        description = field_info.get("description", "")
        field_type = field_info.get("type", "string")
        required = field_name in model_schema.get("required", [])

        schema_fields.append({
            "name": field_name,
            "type": field_type,
            "description": description,
            "required": required,
            "default": field_info.get("default", "None")
        })

    # Format the conversation for the prompt
    conversation_text = "\n".join([
        f"{msg['role'].upper()}: {msg['content']}" for msg in messages
    ])

    # Format existing memories if provided
    existing_memories_text = ""
    if existing_memories and len(existing_memories) > 0:
        existing_memories_text = "EXISTING MEMORIES:\n"
        for i, memory in enumerate(existing_memories):
            existing_memories_text += f"{i+1}. {json.dumps(memory, indent=2)}\n"

    # Create the prompt
    prompt = f"""
You are a memory extraction system. Your task is to extract structured memories from the conversation below.

INSTRUCTIONS:
{instructions}

MEMORY SCHEMA:
The memory should be structured as follows:
{json.dumps(schema_fields, indent=2)}

IMPORTANT: You must create actual memory objects with real values, not just return the schema fields.
Each memory object must include all required fields with appropriate values based on the conversation.

Example of a CORRECT memory object:
```
{{
  "task": "Explaining gradient descent",
  "procedure": "Use a hiking analogy where the hiker is trying to find the lowest point in a valley",
  "context": "When teaching machine learning concepts to non-technical people",
  "effectiveness": 5
}}
```

Example of an INCORRECT memory object (just returning schema fields):
```
{{
  "name": "task",
  "type": "string",
  "description": "The task or situation this procedure applies to",
  "required": true
}}
```

{existing_memories_text}

CONVERSATION:
{conversation_text}

Based on this conversation, extract memories that match the schema. Return ONLY a JSON array of memory objects.
Each memory object should follow the schema exactly. Do not include any explanations or text outside the JSON array.
If no memories can be extracted, return an empty array [].

EXTRACTED MEMORIES (JSON ARRAY):
"""

    # Get the response from the LLM
    response = llm.invoke(prompt)

    # Extract the JSON array from the response
    response_text = response.content

    # Try to find and parse the JSON array
    try:
        # Look for array start and end
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1

        if start_idx >= 0 and end_idx > start_idx:
            json_str = response_text[start_idx:end_idx]
            extracted_data = json.loads(json_str)

            # Validate each memory against the schema
            validated_memories = []
            for memory_data in extracted_data:
                try:
                    # Create an instance of the schema class to validate
                    memory_instance = schema_class(**memory_data)
                    # Convert to dict and add an ID
                    memory_dict = memory_instance.model_dump()
                    memory_dict["id"] = str(uuid.uuid4())
                    validated_memories.append(memory_dict)
                except ValidationError as e:
                    print(f"Validation error for memory: {memory_data}")
                    print(f"Error: {e}")

            return validated_memories
        else:
            print("Could not find JSON array in response")
            return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from response: {e}")
        print(f"Response text: {response_text}")
        return []

def extract_multiple_memory_types(
    llm: ChatBedrockConverse,
    messages: List[Dict[str, str]],
    schema_classes: List[Type[BaseModel]],
    instructions: str,
    existing_memories: Optional[Dict[str, List[Dict[str, Any]]]] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Extract multiple types of structured memories from a conversation.

    Args:
        llm: The language model to use for extraction
        messages: The conversation messages
        schema_classes: List of Pydantic model classes defining the memory structures
        instructions: Instructions for memory extraction
        existing_memories: Optional dictionary of existing memories by type

    Returns:
        A dictionary mapping memory types to lists of extracted memories
    """
    results = {}

    for schema_class in schema_classes:
        schema_name = schema_class.__name__
        existing = existing_memories.get(schema_name, []) if existing_memories else []

        schema_instructions = f"{instructions}\nExtract memories of type: {schema_name}"

        extracted = extract_memories(
            llm=llm,
            messages=messages,
            schema_class=schema_class,
            instructions=schema_instructions,
            existing_memories=existing
        )

        results[schema_name] = extracted

    return results
