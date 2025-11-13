# Services

Domain-based service layer for SurgeonTrainer. Services sit between the API layer and implement business logic.

## Architecture

```
services/
├── common/                 # Shared utilities (config, logging, LLM client)
├── case_intake/           # Case intake and normalization
├── backup/                # Database backup utilities
└── [future services]/     # Other domains as needed
```

## Design Philosophy

**Services vs API:**
- `api/` = I/O layer (FastAPI routes, request/response handling)
- `services/` = Brain (business logic, orchestration, external integrations)
- `api/app/db/` = Storage layer (models, schemas, CRUD)

**Domain-Based Organization:**
Each service is self-contained:
- Own schemas for validation
- Own error types
- Own business logic
- Imports from `common` for shared utilities

## Current Services

### 1. `common/` - Shared Utilities
Shared code used across all services.

**Files:**
- `config.py` - Centralized configuration with environment variable support
- `logging.py` - Structured logging (`get_logger()`, `StructuredLogger`)
- `llm_client.py` - Studio LM API client (`call_studio_lm()`)

**Usage:**
```python
from services.common import get_config, get_logger, call_studio_lm

config = get_config()
log = get_logger(__name__)
response = call_studio_lm(user_prompt="...", system_prompt="...")
```

### 2. `case_intake/` - Case Intake & Normalization
Convert raw surgical notes into structured database records.

**Workflow:**
```
Raw Text → Studio LM → NormalizedCase → Validation → Patient → Encounter → Research Case
```

**Key Files:**
- `schemas.py` - Two-level validation (NormalizedCase → CaseCreatePayload)
- `case_normalizer.py` - LLM integration
- `orchestrator.py` - API coordination
- `test_case_logger.py` - Testing

**Usage:**
```python
from services.case_intake import create_case_from_raw, CaseIntakeError

try:
    result = create_case_from_raw(raw_surgical_note)
    print(f"Created patient {result['patient_id']}")
except CaseIntakeError as e:
    print(f"Intake failed: {e}")
```

See [case_intake/README.md](case_intake/README.md) for details.

### 3. `backup/` - Database Backup
Command-line tool for database backup/restore operations.

**Usage:**
```bash
python -m services.backup backup
python -m services.backup list
python -m services.backup verify <filename>
python -m services.backup restore <filename>
```

See [backup/README.md](backup/README.md) for details.

## Configuration

Services use centralized configuration via `services/common/config.py`.

**Environment Variables:**
All configuration can be overridden with environment variables prefixed with `SURGEON_`:

```bash
# API
SURGEON_API_BASE_URL=http://127.0.0.1:8000
SURGEON_API_TIMEOUT=30

# LLM (Studio LM)
SURGEON_LLM_BASE_URL=http://127.0.0.1:1234
SURGEON_LLM_MODEL=lmstudio-community/qwen2.5-14b-instruct
SURGEON_LLM_TEMPERATURE=0.1
SURGEON_LLM_MAX_TOKENS=2000

# Logging
SURGEON_LOG_LEVEL=INFO
SURGEON_LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

**Defaults:**
All settings have sensible defaults for local development. No `.env` file required to get started.

## Logging

All services use structured logging from `services.common.logging`.

**Standard Logger:**
```python
from services.common import get_logger

log = get_logger(__name__)
log.info("Patient created", extra={"patient_id": 123, "mrn": "12345"})
```

**Structured Logger:**
```python
from services.common.logging import StructuredLogger

log = StructuredLogger(__name__)
log.info("patient_created", patient_id=123, mrn="12345")
# Output: event=patient_created patient_id=123 mrn=12345
```

## Error Handling

Each service domain defines its own error types:
- `CaseIntakeError` - Case intake failures
- `LLMError` - Studio LM API failures
- etc.

All service errors should:
1. Inherit from `Exception`
2. Include descriptive messages
3. Be caught and logged with context
4. Preserve error chain with `from e`

## Adding New Services

1. **Create domain folder:**
   ```bash
   services/your_service/
   ```

2. **Add domain files:**
   ```python
   __init__.py       # Public exports
   schemas.py        # Pydantic models
   service_logic.py  # Business logic
   orchestrator.py   # If coordinating multiple operations
   ```

3. **Import from common:**
   ```python
   from services.common import get_config, get_logger, call_studio_lm
   ```

4. **Update this README** with your service description.

## Testing

Each service should include test files:
- `test_*.py` for standalone testing
- Use real API (not mocks) for integration tests
- Start with `startup_backend.bat` before testing

## Future Services (Ideas)

- `reporting/` - Generate surgical reports
- `analytics/` - Case statistics and trends
- `export/` - Data export (CSV, Excel, FHIR)
- `scheduling/` - OR scheduling logic
- `billing/` - CPT/ICD code validation

## Dependencies

Services layer dependencies are managed at project level in `requirements.txt`:
- `pydantic` - Data validation
- `pydantic-settings` - Configuration
- `requests` - HTTP client
- `python-dotenv` - Optional .env support

No additional service-specific requirements.
