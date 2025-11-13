"""
Tool definitions for the AI agent to interact with the FastAPI backend.
Each tool corresponds to an API endpoint.
"""

def create_patient_tool():
    """Tool for creating a new patient in the system."""
    return {
        "type": "function",
        "function": {
            "name": "create_patient",
            "description": "Create a new patient record in the database. Requires at minimum: MRN, first name, last name, date of birth, and sex.",
            "parameters": {
                "type": "object",
                "properties": {
                    "mrn": {
                        "type": "string",
                        "description": "Medical Record Number - unique identifier for the patient"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Patient's first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Patient's last name"
                    },
                    "date_of_birth": {
                        "type": "string",
                        "description": "Date of birth in YYYY-MM-DD format"
                    },
                    "sex": {
                        "type": "string",
                        "description": "Biological sex",
                        "enum": ["M", "F", "O"]
                    },
                    "email": {
                        "type": "string",
                        "description": "Patient's email address"
                    },
                    "phone": {
                        "type": "string",
                        "description": "Patient's phone number"
                    },
                    "address": {
                        "type": "string",
                        "description": "Street address"
                    },
                    "city": {
                        "type": "string",
                        "description": "City"
                    },
                    "state": {
                        "type": "string",
                        "description": "State abbreviation"
                    },
                    "zip_code": {
                        "type": "string",
                        "description": "ZIP code"
                    }
                },
                "required": ["mrn", "first_name", "last_name", "date_of_birth", "sex"]
            }
        }
    }


def search_patients_tool():
    """Tool for searching existing patients."""
    return {
        "type": "function",
        "function": {
            "name": "search_patients",
            "description": "Search for patients by name, MRN, or other criteria. Returns a list of matching patients.",
            "parameters": {
                "type": "object",
                "properties": {
                    "search": {
                        "type": "string",
                        "description": "Search term (name, MRN, email, phone)"
                    },
                    "skip": {
                        "type": "integer",
                        "description": "Number of records to skip for pagination",
                        "default": 0
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of results to return",
                        "default": 10
                    }
                },
                "required": []
            }
        }
    }


def get_patient_tool():
    """Tool for retrieving a specific patient by ID or MRN."""
    return {
        "type": "function",
        "function": {
            "name": "get_patient",
            "description": "Get detailed information about a specific patient by their ID or MRN.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "integer",
                        "description": "Database ID of the patient"
                    },
                    "mrn": {
                        "type": "string",
                        "description": "Medical Record Number of the patient"
                    }
                },
                "required": []
            }
        }
    }


def update_patient_tool():
    """Tool for updating patient information."""
    return {
        "type": "function",
        "function": {
            "name": "update_patient",
            "description": "Update an existing patient's information. Only provide fields that need to be updated.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "integer",
                        "description": "Database ID of the patient to update"
                    },
                    "email": {"type": "string"},
                    "phone": {"type": "string"},
                    "address": {"type": "string"},
                    "city": {"type": "string"},
                    "state": {"type": "string"},
                    "zip_code": {"type": "string"}
                },
                "required": ["patient_id"]
            }
        }
    }


def create_encounter_tool():
    """Tool for recording a patient encounter."""
    return {
        "type": "function",
        "function": {
            "name": "create_encounter",
            "description": "Record a new encounter/visit for a patient. This is required before adding research case data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {
                        "type": "integer",
                        "description": "Database ID of the patient"
                    },
                    "encounter_date": {
                        "type": "string",
                        "description": "Date of encounter in YYYY-MM-DD format"
                    },
                    "encounter_type": {
                        "type": "string",
                        "description": "Type of encounter (e.g., 'consultation', 'surgery', 'follow-up')"
                    },
                    "chief_complaint": {
                        "type": "string",
                        "description": "Reason for visit"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional clinical notes"
                    }
                },
                "required": ["patient_id", "encounter_date"]
            }
        }
    }


def create_research_case_tool():
    """Tool for creating a research case (surgical procedure)."""
    return {
        "type": "function",
        "function": {
            "name": "create_research_case",
            "description": "Create a research case record for a surgical procedure. Requires encounter_id and procedure type.",
            "parameters": {
                "type": "object",
                "properties": {
                    "procedure_type": {
                        "type": "string",
                        "description": "Type of procedure",
                        "enum": [
                            "rotator-cuff",
                            "knee-surgical", 
                            "shoulder-scope",
                            "shoulder-arthroplasty",
                            "hip-scope",
                            "hip-arthroplasty",
                            "knee-arthroplasty",
                            "other"
                        ]
                    },
                    "encounter_id": {
                        "type": "integer",
                        "description": "ID of the associated encounter"
                    },
                    "fellow_or_pa": {
                        "type": "string",
                        "description": "Fellow or PA performing/assisting"
                    },
                    "attending": {
                        "type": "string",
                        "description": "Attending surgeon"
                    },
                    "mrn": {
                        "type": "string",
                        "description": "Medical Record Number"
                    },
                    "first_name": {
                        "type": "string",
                        "description": "Patient first name"
                    },
                    "last_name": {
                        "type": "string",
                        "description": "Patient last name"
                    },
                    "dob": {
                        "type": "string",
                        "description": "Date of birth (YYYY-MM-DD)"
                    },
                    "surgery_date": {
                        "type": "string",
                        "description": "Surgery date (YYYY-MM-DD)"
                    },
                    "laterality": {
                        "type": "string",
                        "description": "Surgical side",
                        "enum": ["left", "right", "bilateral"]
                    }
                },
                "required": ["procedure_type", "encounter_id"]
            }
        }
    }


def get_patient_stats_tool():
    """Tool for getting patient statistics."""
    return {
        "type": "function",
        "function": {
            "name": "get_patient_stats",
            "description": "Get statistics about all patients in the system (total count, etc.).",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }


def get_all_tools():
    """Returns all available tools for the agent."""
    return [
        create_patient_tool(),
        search_patients_tool(),
        get_patient_tool(),
        update_patient_tool(),
        create_encounter_tool(),
        create_research_case_tool(),
        get_patient_stats_tool()
    ]
