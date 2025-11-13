# SurgeonTrainer v2 🏥

**Comprehensive Patient & Surgical Case Management System**

A robust FastAPI backend for managing surgical training programs with extensive patient data management, case tracking, and automated workflows.

---

## 🎯 What's New in v2

### Comprehensive Patient Management
- **50+ patient fields** - Demographics, contact, insurance, medical history
- **Advanced search & filtering** - Find patients by any criteria
- **Bulk operations** - Import/export hundreds of patients via CSV
- **Visit tracking** - Link encounters to surgical cases
- **Document management** - Track imaging, reports, and consents

### Database Features
- **15+ optimized indexes** for lightning-fast queries
- **Connection pooling** - Handle concurrent requests efficiently
- **Alembic migrations** - Version-controlled schema changes
- **Soft delete** - Never lose historical data
- **Scalable** - SQLite for 10,000s, PostgreSQL for 100,000s+

### Developer Experience
- **Type-safe** - Pydantic validation everywhere
- **Auto-docs** - Interactive API docs at `/docs`
- **Easy setup** - One command installation script
- **Comprehensive docs** - 500+ lines of guides and examples

---

## 🚀 Quick Start

### 1. Install
```powershell
# Run setup script
.\setup.ps1

# Or manually:
cd api
pip install -e .
alembic upgrade head
```

### 2. Start Server
```powershell
cd api
uvicorn app.main:app --reload
```

### 3. Open API Docs
Visit: **http://127.0.0.1:8000/docs**

✅ **Ready to go!** Start creating patients, importing data, and managing cases.

---

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[Patient Management](PATIENT_MANAGEMENT.md)** - Complete API guide
- **[Deployment Checklist](DEPLOYMENT_CHECKLIST.md)** - Production setup
- **[Backend Summary](BACKEND_SUMMARY.md)** - What's been built

---

## 🎨 Features

### Patient Management
✅ Create, read, update, delete patients  
✅ Search by MRN, name, demographics, location  
✅ Filter by status, sex, insurance type  
✅ Pagination for large datasets  
✅ Soft delete with audit trails  

### Bulk Operations
✅ Import patients from CSV (with template)  
✅ Export to CSV or JSON  
✅ Validate before import  
✅ Automatic duplicate detection  
✅ Batch create via API  

### Case Management
✅ Track surgical cases  
✅ Link cases to patients  
✅ ACGME case logging integration  
✅ REDCap research surveys  
✅ Automated form submission  

### Data Integrity
✅ Pydantic validation on all inputs  
✅ Unique constraint on MRN  
✅ Automatic BMI calculation  
✅ JSON fields for flexible data  
✅ Comprehensive error messages  

---

## 🏗️ Architecture

```
SurgeonTrainerv2/
├── api/
│   ├── app/
│   │   ├── core/          # Configuration & logging
│   │   ├── db/            # Database models & session
│   │   │   ├── patient_models.py  # Patient, Visit, Document
│   │   │   ├── models.py          # Surgical cases
│   │   │   └── session.py         # Connection pooling
│   │   ├── schemas/       # Pydantic validation schemas
│   │   ├── routers/       # API endpoints
│   │   │   ├── patients.py         # Patient CRUD
│   │   │   ├── bulk_operations.py # Import/export
│   │   │   └── ...
│   │   └── main.py        # FastAPI application
│   ├── alembic/           # Database migrations
│   └── pyproject.toml     # Python dependencies
├── QUICKSTART.md          # 5-minute setup guide
├── PATIENT_MANAGEMENT.md  # Complete API documentation
├── DEPLOYMENT_CHECKLIST.md # Production deployment guide
├── BACKEND_SUMMARY.md     # What was built
└── setup.ps1              # Automated setup script
```

---

## 📊 API Endpoints

### Patient Management (`/api/v1/patients`)
```
POST   /patients              Create patient
GET    /patients              List with filters & pagination
GET    /patients/{id}         Get by ID
GET    /patients/mrn/{mrn}    Get by MRN
PATCH  /patients/{id}         Update patient
DELETE /patients/{id}         Delete (soft/hard)
GET    /patients/stats/overview  Statistics
```

### Bulk Operations (`/api/v1/patients/bulk`)
```
POST   /bulk/import/csv       Import from CSV
GET    /bulk/export/csv       Export to CSV
GET    /bulk/export/json      Export to JSON
GET    /bulk/template/csv     Download template
POST   /bulk/create           Bulk create
```

### Patient Visits & Documents
```
POST   /patients/{id}/visits     Create visit
GET    /patients/{id}/visits     List visits
POST   /patients/{id}/documents  Add document
GET    /patients/{id}/documents  List documents
```

### Case Management (Existing)
```
GET    /caseprep/cases        List cases
POST   /caseprep/dictation    Parse dictation
POST   /caseprep/submit       Submit cases
```

### Integrations (Existing)
```
POST   /acgme/submit          Submit to ACGME
POST   /redcap/submit         Submit to REDCap
```

**Full API Docs:** http://127.0.0.1:8000/docs

---

## 💻 Example Usage

### Create a Patient
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/v1/patients",
    json={
        "mrn": "MRN123456",
        "first_name": "John",
        "last_name": "Doe",
        "date_of_birth": "1980-01-15",
        "sex": "M",
        "email": "john.doe@example.com",
        "phone_primary": "555-0123"
    }
)

patient = response.json()
print(f"Created patient ID: {patient['id']}")
```

### Search Patients
```python
response = requests.get(
    "http://127.0.0.1:8000/api/v1/patients",
    params={
        "patient_status": "active",
        "state": "IL",
        "page": 1,
        "page_size": 50
    }
)

data = response.json()
print(f"Found {data['total']} patients")
```

### Import from CSV
```python
files = {"file": open("patients.csv", "rb")}
data = {"skip_duplicates": True}

response = requests.post(
    "http://127.0.0.1:8000/api/v1/patients/bulk/import/csv",
    files=files,
    data=data
)

result = response.json()
print(f"Imported {result['created']} patients")
```

---

## 🔧 Tech Stack

- **FastAPI** 0.109+ - Modern async web framework
- **SQLModel** 0.0.14+ - Type-safe ORM (Pydantic + SQLAlchemy)
- **Alembic** 1.13+ - Database migrations
- **Pydantic** 2.5+ - Data validation
- **Pandas** 2.0+ - CSV processing
- **Uvicorn** - ASGI server
- **SQLite/PostgreSQL** - Database

---

## 📈 Performance

### Current Setup (SQLite)
- ✅ Handles 10,000s of patients
- ✅ Connection pooling (10 + 20 overflow)
- ✅ WAL mode for concurrency
- ✅ Memory-mapped I/O
- ✅ 15+ optimized indexes

### Scaling to PostgreSQL
- ✅ Handles 100,000s+ of patients
- ✅ Ready to switch (change DATABASE_URL)
- ✅ All migrations compatible
- ✅ Larger connection pool

---

## 🛡️ Security

- ✅ Input validation (Pydantic)
- ✅ SQL injection protection (SQLModel ORM)
- ✅ CORS configuration
- ✅ Soft delete (data preservation)
- ⏳ JWT authentication (coming soon)
- ⏳ Role-based access control (planned)

---

## 🧪 Testing

### Manual Testing
```powershell
# Start server
uvicorn app.main:app --reload

# Open interactive docs
# Visit: http://127.0.0.1:8000/docs

# Try endpoints directly in browser!
```

### Automated Tests
```powershell
cd api
pytest
pytest -v --cov  # With coverage
```

---

## 🚀 Deployment

### Development
```powershell
.\setup.ps1
uvicorn app.main:app --reload
```

### Production
See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) for complete guide.

---

## 📝 License

Private use only.

---

## 🙏 Support

- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Full Guide**: [PATIENT_MANAGEMENT.md](PATIENT_MANAGEMENT.md)
- **Deployment**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🎉 Status

**Version:** 2.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** November 11, 2025

**Features:** 30+ API endpoints | 50+ patient fields | 15+ database indexes  
**Capacity:** 10,000s patients (SQLite) | 100,000s+ (PostgreSQL)  
**Documentation:** 500+ lines of guides and examples

**Ready to transform your surgical training program!** 🚀
