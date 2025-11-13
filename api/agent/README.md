# 🤖 SurgeonTrainer AI Agent

An intelligent medical assistant that uses local LLMs (via LM Studio) to interact with the SurgeonTrainer FastAPI backend through natural language.

## 🎯 What It Does

The agent acts as a middleware layer that:
1. **Understands natural language** requests from medical staff
2. **Calls your local LLM** (LM Studio) to interpret intent
3. **Executes appropriate API calls** to the FastAPI backend
4. **Returns results** in natural language

## 🏗️ Architecture

```
User Input (Natural Language)
        ↓
   Agent Runner
        ↓
   LM Studio (Local LLM)
        ↓
   Tool Selection & Execution
        ↓
   FastAPI Backend
        ↓
   Database
```

## 📋 Prerequisites

### 1. LM Studio Setup
1. Download [LM Studio](https://lmstudio.ai/)
2. Download a model (recommended: Mistral 7B Instruct v0.2 or Llama 3)
3. Start the local server:
   - Open LM Studio
   - Go to "Local Server" tab
   - Load your model
   - Click "Start Server"
   - Default URL: `http://localhost:1234`

### 2. Backend Running
Make sure your FastAPI backend is running:
```powershell
cd C:\Users\jcf01\SurgeonTrainerv2\api
C:\Users\jcf01\SurgeonTrainerv2\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### 3. Install Dependencies
```powershell
cd C:\Users\jcf01\SurgeonTrainerv2
.\.venv\Scripts\python.exe -m pip install requests
```

## 🚀 Usage

### Start the Agent
```powershell
cd C:\Users\jcf01\SurgeonTrainerv2\api
C:\Users\jcf01\SurgeonTrainerv2\.venv\Scripts\python.exe run_agent.py
```

### Example Conversations

**Add a Patient:**
```
🩺 You: Add a new patient John Doe, born January 15, 1980, male, with abdominal pain

🤖 Assistant: I've created a patient record for John Doe (MRN: MRN123456).
             Patient ID: 1, Status: Active
```

**Search Patients:**
```
🩺 You: Find all active patients

🤖 Assistant: Found 5 active patients:
             1. John Doe (MRN123456)
             2. Jane Smith (MRN234567)
             ...
```

**Get Patient Info:**
```
🩺 You: Show me details for MRN123456

🤖 Assistant: Patient: John Doe
             MRN: MRN123456
             DOB: 1980-01-15
             Status: Active
             Chief Complaint: Abdominal pain
```

**Record a Visit:**
```
🩺 You: Record a follow-up visit for patient ID 1 today with diagnosis "appendicitis"

🤖 Assistant: Visit recorded successfully. Visit ID: 5
```

**Get Statistics:**
```
🩺 You: How many patients do we have?

🤖 Assistant: System Statistics:
             Total Active: 45
             Total Admitted: 3
             Total Discharged: 12
```

## 🛠️ Configuration

Copy `.env.example` to `.env` and customize:

```env
# LM Studio Configuration
LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
LM_STUDIO_MODEL=mistral-7b-instruct-v0.2

# Backend API
BACKEND_URL=http://localhost:8000

# Agent Settings
AGENT_TEMPERATURE=0.3  # Lower = more focused, Higher = more creative
DEBUG=true             # Enable detailed logging
```

## 📦 Files Structure

```
agent/
├── __init__.py           # Package marker
├── agent_runner.py       # Main agent logic & LLM orchestration
├── tools.py              # Tool definitions (functions the LLM can call)
├── config.py             # Configuration & environment variables
├── prompts.py            # System prompts & examples for the LLM
└── README.md            # This file

run_agent.py             # Interactive CLI script
```

## 🔧 How It Works

### 1. Tool Definitions (`tools.py`)
Defines what actions the agent can take:
- `create_patient` - Add new patients
- `search_patients` - Find patients by criteria
- `get_patient` - Get detailed patient info
- `update_patient` - Modify patient records
- `create_visit` - Record patient visits
- `get_patient_stats` - System statistics

### 2. Agent Runner (`agent_runner.py`)
Orchestrates the workflow:
1. Receives user input
2. Sends to LM Studio with available tools
3. LLM decides which tool(s) to call
4. Executes API calls to backend
5. Sends results back to LLM
6. Returns natural language response

### 3. Prompts (`prompts.py`)
Guides the LLM's behavior:
- System role (medical assistant)
- Guidelines (HIPAA awareness, date parsing)
- Example interactions

## 🎨 Customization

### Add New Tools
1. Define tool in `tools.py`:
```python
def my_new_tool():
    return {
        "type": "function",
        "function": {
            "name": "my_tool",
            "description": "What it does",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string"}
                }
            }
        }
    }
```

2. Add to `get_all_tools()`:
```python
def get_all_tools():
    return [
        create_patient_tool(),
        my_new_tool(),  # Add here
        # ...
    ]
```

3. Handle in `execute_tool()` in `agent_runner.py`:
```python
elif tool_name == "my_tool":
    url = get_full_url("/my-endpoint")
    response = requests.get(url, params=arguments)
```

### Modify Agent Behavior
Edit `prompts.py` to change:
- Personality/tone
- Medical knowledge emphasis
- Response format
- Security guidelines

## 🐛 Troubleshooting

### "Failed to call LLM"
- Check LM Studio is running: http://localhost:1234
- Verify model is loaded in LM Studio
- Check firewall settings

### "API call failed"
- Ensure FastAPI backend is running
- Check backend URL in `.env`
- Verify API endpoints exist

### Agent gives incorrect responses
- Try different model in LM Studio
- Adjust `AGENT_TEMPERATURE` (lower for more precise)
- Add more examples to `prompts.py`

### Debug Mode
Enable detailed logging:
```env
DEBUG=true
```

## 📊 Supported Models

Tested with:
- ✅ Mistral 7B Instruct v0.2 (recommended)
- ✅ Llama 3 8B Instruct
- ✅ Qwen 2.5 7B Instruct
- ✅ Phi-3 Medium

Requirements:
- Must support function/tool calling
- ~8GB VRAM for 7B models
- ~16GB VRAM for 13B models

## 🔒 Security Notes

- Agent runs locally - no cloud API calls
- HIPAA considerations:
  - All data stays on your infrastructure
  - No PHI sent to external services
  - Audit logs available in FastAPI backend
- Use authentication for production (add JWT token passing)

## 🚀 Next Steps

- [ ] Add conversation memory (save chat history)
- [ ] Implement multi-turn conversations
- [ ] Add voice input/output
- [ ] Create web UI for the agent
- [ ] Add authentication/authorization
- [ ] Implement specialized medical knowledge base
- [ ] Add support for medical imaging queries

## 📚 Resources

- [LM Studio Documentation](https://lmstudio.ai/docs)
- [FastAPI Backend Docs](http://localhost:8000/docs)
- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)

---

**Happy Healing! 🏥**
