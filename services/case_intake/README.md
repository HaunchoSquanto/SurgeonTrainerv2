# Case Intake Service

Domain-based service for converting raw surgical dictation/notes into structured database records using LLM normalization.

## Architecture

```
services/
├── common/                      # Shared utilities
│   ├── config.py               # Centralized configuration
│   ├── logging.py              # Structured logging
│   └── llm_client.py           # Studio LM wrapper
└── case_intake/                # Case intake domain
    ├── schemas.py              # Pydantic models (NormalizedCase, CaseCreatePayload)
    ├── case_normalizer.py      # LLM normalization logic
    ├── orchestrator.py         # Workflow coordination
    └── test_case_logger.py     # Test script
```

## Workflow

```
Raw Text → Studio LM → NormalizedCase → Validation → CaseCreatePayload
         ↓
    API Calls: Patient → Encounter → Research Case → Success
```

## Schemas

### 1. NormalizedCase (LLM Output)
Lenient schema - what Studio LM extracts from raw text.
- **Required**: mrn, first_name, last_name, date_of_birth, sex, surgery_date, procedure_type
- **Optional**: middle_name, laterality, attending, fellow_or_pa, chief_complaint, location, notes

### 2. CaseCreatePayload (DB Input)
Strict schema - enforces hard requirements before database insert.
- Validates all required fields are present
- Converts enums to string values
- Acts as gatekeeper between normalization and DB

## Files

- **`schemas.py`** - Pydantic models for normalization and validation
- **`case_normalizer.py`** - Studio LM integration for text extraction
- **`orchestrator.py`** - Workflow coordination (patient → encounter → research case)
- **`test_case_logger.py`** - Test script with example surgical note

## Configuration

Set environment variables (optional - has defaults):

```bash
# API Configuration
SURGEON_API_BASE_URL=http://127.0.0.1:8000
SURGEON_API_TIMEOUT=30

# Studio LM Configuration
SURGEON_LLM_BASE_URL=http://127.0.0.1:1234
SURGEON_LLM_MODEL=lmstudio-community/qwen2.5-14b-instruct
SURGEON_LLM_TEMPERATURE=0.1
SURGEON_LLM_MAX_TOKENS=2000

# Logging
SURGEON_LOG_LEVEL=INFO
```

## Required Fields

The LLM **must** extract these fields from the raw text:

- `mrn` - Medical record number
- `first_name` - Patient first name
- `last_name` - Patient last name
- `date_of_birth` - Format: YYYY-MM-DD
- `sex` - M, F, or O
- `surgery_date` - Format: YYYY-MM-DD
- `procedure_type` - One of: rotator-cuff, knee-surgical, shoulder-scope, shoulder-arthroplasty, hip-scope, hip-arthroplasty, knee-arthroplasty, other

## Optional Fields

- `middle_name`
- `laterality` - Right, Left, or Bilateral
- `attending` - Attending surgeon name
- `fellow_or_pa` - Fellow or PA name
- `chief_complaint` - Reason for visit
- `location` - Hospital/facility name
- `notes` - Additional clinical notes

## Usage

1. **Start Studio LM** (if not already running):
   ```bash
   # Studio LM should be running on http://127.0.0.1:1234
   ```

2. **Start the API server:**
   ```bash
   startup_backend.bat
   ```

3. **Run test:**
   ```bash
   # From project root
   python -m services.case_intake.test_case_logger
   ```

4. **Use in code:**
   ```python
   from services.case_intake import create_case_from_raw, CaseIntakeError

   raw_note = """
   Patient: John Smith
   MRN: 12345678
   DOB: 1985-03-15
   ...
   """

   try:
       result = create_case_from_raw(raw_note)
       print(f"Created patient ID: {result['patient_id']}")
       print(f"Created encounter ID: {result['encounter_id']}")
       print(f"Created research case ID: {result['research_case_id']}")
   except CaseIntakeError as e:
       print(f"Intake failed: {e}")
   ```

## API Endpoints Used

1. `GET /api/v1/patients?search={mrn}` - Search for existing patient
2. `POST /api/v1/patients` - Create new patient
3. `POST /api/v1/encounters` - Create encounter
4. `POST /api/v1/rc/{procedure_type}` - Create research case

## Error Handling

- **`CaseIntakeError`**: Raised when any step of the intake workflow fails
- **`ValueError`**: Raised by normalizer if LLM returns invalid data
- **`ValidationError`**: Raised if Pydantic schema validation fails

All errors include detailed messages and are logged with structured logging.

## Design Principles

1. **Separation of Concerns**
   - `case_normalizer.py` = LLM interaction only
   - `orchestrator.py` = API coordination only
   - `schemas.py` = Data validation only

2. **Two-Level Validation**
   - `NormalizedCase` = Lenient (what LLM tries to give)
   - `CaseCreatePayload` = Strict (what DB requires)
   - Conversion function acts as gatekeeper

3. **Structured Logging**
   - All operations logged with context
   - Easy to trace workflow through logs
   - `event=operation_name key=value` format

4. **Configuration Management**
   - Centralized in `services/common/config.py`
   - Environment variable overrides
   - Sensible defaults for dev

## Notes

- The service first searches for existing patients by MRN to avoid duplicates
- All research case fields (except `encounter_id`) are optional
- The raw note text is preserved in the returned data for auditing
