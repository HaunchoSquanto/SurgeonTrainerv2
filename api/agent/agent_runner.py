"""
AI Agent Runner - connects LM Studio LLM with FastAPI backend.
"""
import json
import requests
from datetime import datetime
from typing import Dict, Any, List, Optional
from agent.tools import get_all_tools
from agent.config import (
    LM_STUDIO_URL, 
    LM_STUDIO_MODEL, 
    BACKEND_URL, 
    API_PREFIX,
    AGENT_TEMPERATURE,
    TIMEOUT,
    DEBUG,
    get_full_url
)
from agent.prompts import get_system_message


def call_llm(messages: List[Dict[str, str]], tools: Optional[List[Dict]] = None) -> Dict[str, Any]:
    """
    Call LM Studio API with messages and tools.
    
    Args:
        messages: Conversation history
        tools: Available tools for function calling
        
    Returns:
        LLM response with potential tool calls
    """
    # Some models don't support system role with tools - convert system to user message
    processed_messages = []
    for msg in messages:
        if msg["role"] == "system" and tools:
            # Convert system message to user message for compatibility
            processed_messages.append({
                "role": "user",
                "content": f"[System Instructions]\n{msg['content']}\n\nPlease acknowledge these instructions."
            })
            processed_messages.append({
                "role": "assistant",
                "content": "Understood. I will follow these instructions."
            })
        else:
            processed_messages.append(msg)
    
    payload = {
        "model": LM_STUDIO_MODEL,  # Required when multiple models loaded
        "messages": processed_messages,
        "temperature": AGENT_TEMPERATURE,
        "max_tokens": 2000,
        "stream": False
    }
    
    # Only add tools if the model supports them
    if tools and len(processed_messages) > 1:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
    
    if DEBUG:
        print(f"\n[DEBUG] Calling LLM: {LM_STUDIO_URL}")
        print(f"[DEBUG] Messages: {len(processed_messages)} messages")
        if tools:
            print(f"[DEBUG] Tools: {len(tools)} available")
    
    try:
        response = requests.post(LM_STUDIO_URL, json=payload, timeout=TIMEOUT)
        
        if DEBUG:
            print(f"[DEBUG] Response Status: {response.status_code}")
        
        # Check for errors
        if response.status_code != 200:
            error_text = response.text
            if DEBUG:
                print(f"[DEBUG] Error Response: {error_text[:200]}...")
            
            # If tools caused the error, retry without them
            if tools and ("tool" in error_text.lower() or "function" in error_text.lower()):
                if DEBUG:
                    print("[DEBUG] Retrying without tools (model may not support function calling)")
                payload.pop("tools", None)
                payload.pop("tool_choice", None)
                response = requests.post(LM_STUDIO_URL, json=payload, timeout=TIMEOUT)
        
        response.raise_for_status()
        result = response.json()
        
        if DEBUG:
            print(f"[DEBUG] ✅ LLM Response received successfully")
        
        return result
    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to call LLM: {str(e)}"
        if DEBUG:
            print(f"[DEBUG] ❌ Exception: {error_msg}")
        
        return {
            "error": error_msg,
            "choices": [{
                "message": {
                    "content": f"Sorry, I couldn't connect to the AI model. Error: {str(e)}"
                }
            }]
        }


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a tool by calling the appropriate backend endpoint.
    
    Args:
        tool_name: Name of the tool to execute
        arguments: Arguments for the tool
        
    Returns:
        Result from the API call
    """
    if DEBUG:
        print(f"[DEBUG] Executing tool: {tool_name}")
        print(f"[DEBUG] Arguments: {json.dumps(arguments, indent=2)}")
    
    try:
        # Map tool names to API endpoints
        if tool_name == "create_patient":
            url = get_full_url("/patients")
            response = requests.post(url, json=arguments, timeout=TIMEOUT)
            
        elif tool_name == "search_patients":
            url = get_full_url("/patients")
            response = requests.get(url, params=arguments, timeout=TIMEOUT)
            
        elif tool_name == "get_patient":
            if "mrn" in arguments:
                url = get_full_url(f"/patients/mrn/{arguments['mrn']}")
            elif "patient_id" in arguments:
                url = get_full_url(f"/patients/{arguments['patient_id']}")
            else:
                return {"error": "Either patient_id or mrn is required"}
            response = requests.get(url, timeout=TIMEOUT)
            
        elif tool_name == "update_patient":
            patient_id = arguments.pop("patient_id")
            url = get_full_url(f"/patients/{patient_id}")
            response = requests.patch(url, json=arguments, timeout=TIMEOUT)
            
        elif tool_name == "create_visit":
            patient_id = arguments.pop("patient_id")
            url = get_full_url(f"/patients/{patient_id}/visits")
            response = requests.post(url, json=arguments, timeout=TIMEOUT)
            
        elif tool_name == "get_patient_stats":
            url = get_full_url("/patients/stats/overview")
            response = requests.get(url, timeout=TIMEOUT)
            
        else:
            return {"error": f"Unknown tool: {tool_name}"}
        
        if DEBUG:
            print(f"[DEBUG] API URL: {url}")
            print(f"[DEBUG] Response Status: {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        
        if DEBUG:
            print(f"[DEBUG] Tool result: {json.dumps(result, indent=2)}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API call failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                error_msg += f" - {json.dumps(error_detail)}"
                if DEBUG:
                    print(f"[DEBUG] API Error: {error_msg}")
            except:
                error_msg += f" - {e.response.text}"
                if DEBUG:
                    print(f"[DEBUG] API Error: {error_msg}")
        else:
            if DEBUG:
                print(f"[DEBUG] Connection Error: {error_msg}")
        return {"error": error_msg}


def run_agent(user_input: str, conversation_history: Optional[List[Dict]] = None) -> str:
    """
    Main agent loop - processes user input and orchestrates LLM + tool calls.
    
    Args:
        user_input: User's message
        conversation_history: Optional previous conversation context
        
    Returns:
        Agent's response as a string
    """
    # Initialize conversation
    if conversation_history is None:
        messages = [
            {"role": "system", "content": get_system_message()},
        ]
    else:
        messages = conversation_history
    
    # Add user message
    messages.append({"role": "user", "content": user_input})
    
    # Get all available tools
    tools = get_all_tools()
    
    # Try with tools first
    llm_response = call_llm(messages, tools)
    
    # Check for errors
    if "error" in llm_response:
        return llm_response.get("choices", [{}])[0].get("message", {}).get("content", "Error occurred")
    
    # Get assistant message
    assistant_message = llm_response["choices"][0]["message"]
    
    # Check if response has tool_calls (some models return empty array even if not supported)
    tool_calls = assistant_message.get("tool_calls", [])
    
    # If model returned content but no tool calls, it might not support function calling
    # Parse the response to see if we should execute any tools manually
    if not tool_calls and "content" in assistant_message:
        content = assistant_message["content"].lower()
        
        # Simple keyword-based tool detection for models without function calling
        if any(word in content for word in ["create", "add", "new patient"]):
            # For now, just return the LLM's response
            # TODO: Implement manual tool parsing
            return assistant_message["content"]
        
        return assistant_message["content"]
    
    messages.append(assistant_message)
    
    # Execute tool calls if present
    if tool_calls:
        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            
            # Parse arguments (may be string or dict)
            arguments = tool_call["function"]["arguments"]
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except json.JSONDecodeError:
                    try:
                        arguments = eval(arguments)  # Fallback for Python dict strings
                    except:
                        arguments = {}
            
            # Execute the tool
            tool_result = execute_tool(function_name, arguments)
            
            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.get("id", "default"),
                "name": function_name,
                "content": json.dumps(tool_result)
            })
        
        # Call LLM again with tool results to get final response
        # This time without tools to avoid issues
        final_response = call_llm(messages, tools=None)
        return final_response["choices"][0]["message"]["content"]
    
    # No tool calls, return direct response
    return assistant_message.get("content", "I'm not sure how to respond to that.")


def run_agent_with_context(user_input: str, messages: List[Dict]) -> tuple[str, List[Dict]]:
    """
    Run agent and return both response and updated conversation history.
    
    Args:
        user_input: User's message
        messages: Current conversation history
        
    Returns:
        Tuple of (response, updated_messages)
    """
    response = run_agent(user_input, messages)
    return response, messages

