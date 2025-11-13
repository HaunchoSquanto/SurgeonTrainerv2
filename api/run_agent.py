"""
Interactive CLI for the SurgeonTrainer AI Agent.
Run this script to chat with the agent and manage patients via natural language.
"""
from agent.agent_runner import run_agent
from agent.config import DEBUG
import sys

print("=" * 60)
print("🩺 SurgeonTrainer AI Medical Assistant")
print("=" * 60)
print("\nI can help you:")
print("  • Add new patients")
print("  • Search for patients")
print("  • Update patient information")
print("  • Record patient visits")
print("  • Get system statistics")
print("\nType 'exit' or 'quit' to end the session.")
print("=" * 60)
print()

# Maintain conversation history for context
conversation_history = []

while True:
    try:
        user_input = input("🩺 You: ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
            print("\n👋 Goodbye! Stay safe and keep healing!")
            break
        
        # Get response from agent
        response = run_agent(user_input, conversation_history if conversation_history else None)
        
        print(f"🤖 Assistant: {response}\n")
        
    except KeyboardInterrupt:
        print("\n\n👋 Session interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        print()

