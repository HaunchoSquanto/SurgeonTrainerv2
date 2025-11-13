# FellowTrainer - Surgical Case Management System

**Status**: ✅ **FULL STACK DEPLOYED & RUNNING** (November 9, 2025)

Automated system for managing surgical cases, integrating with ACGME case logging and REDCap research surveys. Features dictation parsing, AI-powered data extraction, and browser automation for form submission.

---

## 🎯 What is FellowTrainer?

A comprehensive automation system that:

1. **Parses surgical case information** from compliance emails or dictation
2. **Extracts structured data** using AI (GPT-4o)
3. **Manages case database** with validation and tracking
4. **Automates ACGME submissions** to case logging system
5. **Automates REDCap submissions** to research database
6. **Prevents duplicates** via persistent database tracking

**Time Saved**: ~45 min/week with ACGME + 2 hours/week with REDCap = **2.75 hours/week** of automation

---

## 🚀 Quick Start (NEW: Web Interface)

### Option 1: Web Interface (Recommended for New Users)

**Start Backend API** (Terminal 1):
```powershell
cd C:\Projects\FellowTrainer\api
C:\Projects\workflows\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```
✅ API running at http://127.0.0.1:8000

**Start Frontend UI** (Terminal 2):
```powershell
cd C:\Projects\FellowTrainer\ui
npm run dev
```
✅ UI running at http://localhost:5173

**Open in Browser**:
- **Main App**: http://localhost:5173
- **API Docs**: http://127.0.0.1:8000/docs

### Option 2: Direct REDCap Workflow (Legacy)

```powershell
# Quick launch
start_redcap.bat

# Or via Python
python redcap_email_workflow.py
```

---

## 🎨 Web Interface Overview

### Tab 1: Case Database
- View all cases in database
- Filter by status (pending, submitted, failed)
- Filter by anatomical region (shoulder, knee, hip, etc)
- Pagination support (20 cases per page)
- Delete cases
- View case details

### Tab 2: Case Prep Dictation
- Enter free-form surgical case dictation
- Click "Parse Dictation" to extract structured data
- Review extracted fields
- View missing information checklist
- See extracted cases ready for submission

### Tab 3: ACGME Submit
- View pending ACGME cases from database
- Multi-select cases for batch submission
- Submit to ACGME case logger
- View submission results and status

### Tab 4: REDCap Submit
- Mode 1: Select individual cases
- Mode 2: Paste compliance email (auto-extract cases)
- Submit to REDCap surveys
- Track submission status

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FellowTrainer                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Web UI (React + Vite)                      │  │
│  │        http://localhost:5173                         │  │
│  │   • Case Database  • Case Prep  • ACGME  • REDCap   │  │
│  └────────────────────────┬─────────────────────────────┘  │
│                           │                                  │
│                    HTTP API (Axios)                         │
│                           │                                  │
│  ┌────────────────────────▼─────────────────────────────┐  │
│  │        FastAPI Backend (Python 3.12.7)              │  │
│  │        http://127.0.0.1:8000/api/v1                 │  │
│  │                                                       │  │
│  │  • Health Checks      • Case Management             │  │
│  │  • ACGME Integration  • REDCap Integration          │  │
│  │  • Workflow Bridge    • Database Session            │  │
│  │                                                       │  │
│  │  SQLModel ORM ──→ SQLite Database                   │  │
│  │                                                       │  │
│  │  Workflow Bridge ──→ Existing Modules              │  │
│  │  • DictationNormalizer  (parse dictation)          │  │
│  │  • CasePrepValidator    (validate data)            │  │
│  │  • AIClient             (GPT integration)           │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 Installation & Setup

### Prerequisites

- **Python 3.12.7** (via C:\Projects\workflows\.venv)
- **Node.js 20.10.0+** (from https://nodejs.org)
- **OpenAI API Key** (for GPT models)

### 1. Backend Setup

```powershell
# Navigate to API directory
cd C:\Projects\FellowTrainer\api

# Install dependencies (already done if running)
pip install -e .

# Configure environment
copy .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 2. Frontend Setup

```powershell
# Navigate to UI directory
cd C:\Projects\FellowTrainer\ui

# Install dependencies (already done if running)
npm install

# Start development server
npm run dev
```

### 3. Run Both

```powershell
# Terminal 1 - Start API
cd C:\Projects\FellowTrainer\api
C:\Projects\workflows\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Terminal 2 - Start UI
cd C:\Projects\FellowTrainer\ui
npm run dev

# Open http://localhost:5173
```

---

## 🔌 API Endpoints

### Health & Status
```
GET  /api/v1/healthz                 - Basic health check
GET  /api/v1/readyz                  - Readiness check (includes DB)
```

### Case Management
```
GET  /api/v1/caseprep/cases          - List cases (paginated)
GET  /api/v1/caseprep/cases/{id}     - Get specific case
POST /api/v1/caseprep/dictation      - Parse dictation → cases
POST /api/v1/caseprep/merge          - Merge case updates
POST /api/v1/caseprep/submit         - Submit cases
DEL  /api/v1/caseprep/cases/{id}     - Delete case
```

### ACGME Integration
```
GET  /api/v1/acgme/pending           - List pending ACGME cases
POST /api/v1/acgme/submit            - Submit to ACGME
GET  /api/v1/acgme/status/{id}       - Get submission status
```

### REDCap Integration
```
GET  /api/v1/redcap/pending          - List pending REDCap cases
POST /api/v1/redcap/submit           - Submit to REDCap
POST /api/v1/redcap/compliance-email - Process compliance email
GET  /api/v1/redcap/status/{id}      - Get submission status
```

**Interactive Documentation**: http://127.0.0.1:8000/docs

---

## 📋 How It Works

### REDCap Email-to-Form Workflow

```
1. Compliance Email Received
   ↓
2. Parse Email → Extract MRN, Attending, DOS
   ↓
3. Look Up Patient Case Details
   ↓
4. Record Audio Dictation of Case
   ↓
5. Transcribe Audio (Whisper-1)
   ↓
6. Extract Structured Data (GPT-4o)
   ↓
7. Review & Approve Extraction
   ↓
8. Auto-Fill REDCap Survey Form
   ↓
9. Submit Survey
   ↓
10. Mark Case as Completed in Database
```

### ACGME Case Logging Workflow

```
1. Case Data Imported
   ↓
2. Validate Case Completeness
   ↓
3. Check for Duplicates
   ↓
4. Preview Cases
   ↓
5. Submit to ACGME
   ↓
6. Update Database with Status
```

---

## 🗂️ Project Structure

```
FellowTrainer/
│
├── api/                              # FastAPI Backend
│   ├── app/
│   │   ├── core/                    # Config, security, dependencies
│   │   ├── db/                      # SQLModel models, session
│   │   ├── schemas/                 # Pydantic request/response schemas
│   │   ├── routers/                 # API endpoints
│   │   ├── services/                # Business logic, workflow bridge
│   │   ├── tests/                   # Pytest tests
│   │   └── main.py                  # FastAPI application
│   ├── pyproject.toml               # Python dependencies
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Template
│   └── README.md                    # API documentation
│
├── ui/                              # React Frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── lib/                    # API client, types
│   │   ├── App.tsx                 # Main app
│   │   └── main.tsx                # React entry point
│   ├── package.json                # Node dependencies
│   ├── vite.config.ts              # Vite config
│   └── README.md                   # UI documentation
│
├── workflows/                       # Existing workflow modules
│   ├── caseprep/                   # Case preparation
│   ├── acgme/                      # ACGME automation
│   └── redcap/                     # REDCap automation
│
├── integrations/                    # External service clients
│   ├── audio_recorder.py           # Audio + Whisper
│   ├── redcap_client.py            # REDCap browser automation
│   ├── acgme_client.py             # ACGME browser automation
│   └── outlook_client.py           # Email parsing
│
├── data/                           # Database & data utilities
│   ├── database.py                 # Case tracking
│   └── acgme_database.py           # ACGME tracking
│
├── core/                           # Core workflow engine
│   ├── workflow.py                 # Base orchestrator
│   ├── task.py                     # Task abstraction
│   ├── executor.py                 # Execution engine
│   └── ai_client.py                # OpenAI wrapper
│
├── DEPLOYMENT_STATUS.md            # Current deployment status
├── DEVELOPER_GUIDE.md              # Development reference
├── PROJECT_REFERENCE.md            # Complete project reference
├── ARCHITECTURE.md                 # Architecture documentation
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

---

## 📊 Technology Stack

### Backend
- **Framework**: FastAPI 0.121.1 (async Python web framework)
- **ORM**: SQLModel 0.0.27 (Pydantic + SQLAlchemy)
- **Database**: SQLite (upgradeable to PostgreSQL)
- **Server**: Uvicorn 0.38.0 (ASGI)
- **Validation**: Pydantic 2.12.4
- **Config**: pydantic-settings 2.11.0
- **AI**: OpenAI 2.7.1 (GPT-4o, Whisper-1)
- **Security**: Python-jose 3.5.0 + passlib 1.7.4

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **State Management**: React Query (TanStack Query)
- **Language**: TypeScript
- **Styling**: CSS (Tailwind configured)

### Browser Automation
- **Playwright** (Chromium) - Form submission, ACGME/REDCap
- **Whisper-1** - Audio transcription
- **GPT-4o** - Data extraction

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=sqlite:///./fellowtrainer.db

# OpenAI API Key (required)
OPENAI_API_KEY=sk-proj-xxxxx

# CORS - Must be JSON array format
ALLOWED_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# JWT (for future authentication)
JWT_SECRET=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
DEBUG=true
```

---

## 📚 Documentation

- **`DEPLOYMENT_STATUS.md`** - Current system status and running services
- **`DEVELOPER_GUIDE.md`** - Development reference for backend/frontend
- **`PROJECT_REFERENCE.md`** - Complete project architecture and workflows
- **`ARCHITECTURE.md`** - System design and file organization
- **`api/README.md`** - API-specific documentation
- **`ui/README.md`** - UI-specific documentation

---

## 🧪 Testing

### API Tests
```powershell
cd api
pytest                    # Run all tests
pytest -v               # Verbose output
pytest --cov            # Coverage report
```

### Manual API Testing
- Use Swagger UI: http://127.0.0.1:8000/docs
- Or curl commands:
```powershell
curl http://127.0.0.1:8000/api/v1/healthz
curl http://127.0.0.1:8000/api/v1/caseprep/cases
```

### UI Testing
- Open http://localhost:5173
- Navigate tabs
- Test all features

---

## 🚀 Deployment

### Development
```powershell
# Terminal 1
cd C:\Projects\FellowTrainer\api
C:\Projects\workflows\.venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Terminal 2
cd C:\Projects\FellowTrainer\ui
npm run dev
```

### Production
See `DEPLOYMENT_STATUS.md` for production setup instructions.

---

## 🐛 Troubleshooting

### API won't start
1. Check Python version: `python --version` (should be 3.12.7)
2. Check dependencies: `pip install -e api/`
3. Check port: `netstat -ano | findstr :8000`

### UI won't load
1. Check Node.js: `node --version`
2. Install dependencies: `npm install`
3. Check port: `netstat -ano | findstr :5173`

### Database errors
1. Delete `api/fellowtrainer.db`
2. Restart API - tables auto-recreate

### CORS errors
1. Verify `ALLOWED_ORIGINS` in `api/.env` is JSON array
2. Example: `["http://localhost:5173","http://localhost:3000"]`

---

## 📞 Next Steps

### Immediate Tasks
1. ✅ API Backend - RUNNING
2. ✅ React Frontend - RUNNING
3. ⏳ Implement workflow integration TODOs
4. ⏳ Add user authentication
5. ⏳ Complete ACGME/REDCap integration

### Future Enhancements
- Real-time updates with WebSockets
- Background job processing (Celery)
- Admin dashboard
- Analytics and reporting
- Mobile app support

---

## 📝 License

Private use only.

---

## 🙋 Support

For questions or issues:
1. Check documentation files listed above
2. Review error messages in terminal/browser console
3. Check `DEPLOYMENT_STATUS.md` for current system status
4. See `DEVELOPER_GUIDE.md` for debugging tips

---

**Last Updated**: November 9, 2025  
**Status**: ✅ Full stack deployed and running
