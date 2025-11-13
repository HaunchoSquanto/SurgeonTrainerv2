# 🤖 Quick Start Guide - AI Agent Setup

## Step-by-Step Setup

### 1. Install LM Studio
1. Download from: https://lmstudio.ai/
2. Install and open LM Studio
3. Download a model (click "Search" tab):
   - **Recommended**: `mistralai/Mistral-7B-Instruct-v0.2-GGUF`
   - Alternative: `meta-llama/Meta-Llama-3-8B-Instruct-GGUF`
4. Start the local server:
   - Click "Local Server" tab (left sidebar)
   - Select your downloaded model
   - Click **"Start Server"**
   - Confirm it shows: `Server running at http://localhost:1234`

### 2. Start Your FastAPI Backend
Open a **NEW** PowerShell terminal:
```powershell
cd C:\Users\jcf01\SurgeonTrainerv2\api
C:\Users\jcf01\SurgeonTrainerv2\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

Leave this running! ✅

### 3. Run the AI Agent
Open **ANOTHER** PowerShell terminal:
```powershell
cd C:\Users\jcf01\SurgeonTrainerv2\api
C:\Users\jcf01\SurgeonTrainerv2\.venv\Scripts\python.exe run_agent.py
```

### 4. Test It! 🎉

Try these commands:

**Create a patient:**
```
Add a new patient John Doe, born January 15, 1980, male, chief complaint is abdominal pain
```

**Search:**
```
Find all active patients
```

**Get stats:**
```
How many patients do we have in the system?
```

**Record visit:**
```
Record a consultation visit for patient ID 1 today
```

## Architecture

```
┌─────────────────┐
│   User Input    │  "Add patient John Doe..."
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  run_agent.py   │  CLI Interface
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ agent_runner.py │  Orchestrator
└────────┬────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│   LM Studio     │  │  FastAPI        │
│   (Local LLM)   │  │  Backend        │
│  localhost:1234 │  │  localhost:8000 │
└─────────────────┘  └────────┬────────┘
                              │
                              ▼
                     ┌─────────────────┐
                     │   SQLite DB     │
                     │  (Patients)     │
                     └─────────────────┘
```

## Configuration

If you need to change settings, create `api/agent/.env`:

```env
LM_STUDIO_URL=http://localhost:1234/v1/chat/completions
LM_STUDIO_MODEL=mistral-7b-instruct-v0.2
BACKEND_URL=http://localhost:8000
AGENT_TEMPERATURE=0.3
DEBUG=false
```

## Troubleshooting

### "Failed to call LLM"
❌ LM Studio not running
✅ Open LM Studio → Local Server → Start Server

### "API call failed"
❌ Backend not running
✅ Start backend: `uvicorn app.main:app --reload`

### "Connection refused"
❌ Wrong ports
✅ Check LM Studio shows port 1234
✅ Check backend shows port 8000

### Agent responds slowly
💡 First request is always slow (model loading)
💡 Subsequent requests should be fast (2-5 seconds)

### Model not found
❌ Model not downloaded in LM Studio
✅ LM Studio → Search → Download model → Load in Local Server

## Next Steps

Once working:
1. Try complex queries: "Find all male patients over 50"
2. Chain operations: "Create patient then schedule visit"
3. Update records: "Change patient 1's email to new@email.com"
4. Read the full docs: `api/agent/README.md`

---

**Need help? Check the logs by setting `DEBUG=true` in `.env`**
