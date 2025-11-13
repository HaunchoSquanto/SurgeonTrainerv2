"""
Orchestrator for case intake workflow.
Coordinates: LLM normalization → Patient creation → Encounter creation → Research case creation
"""
import requests
from typing import Dict, Any
from services.common import get_config, get_logger
from .schemas import NormalizedCase, CaseCreatePayload, normalized_to_case_payload
from .case_normalizer import normalize_free_text_to_case

log = get_logger(__name__)


class CaseIntakeError(Exception):
    """Raised when case intake workflow fails"""
    pass


def create_case_from_raw(raw_text: str) -> Dict[str, Any]:
    """
    Complete case intake workflow from raw text to database.
    
    Steps:
    1. Normalize raw text with LLM
    2. Validate and convert to strict payload
    3. Search for or create patient
    4. Create encounter
    5. Create research case
    
    Args:
        raw_text: Raw surgical note/dictation
    
    Returns:
        dict with created IDs and metadata:
        {
            "success": bool,
            "patient_id": int,
            "encounter_id": int,
            "research_case_id": int,
            "procedure_type": str,
            "raw_note": str
        }
    
    Raises:
        CaseIntakeError: If any step fails
    """
    config = get_config()
    log.info("Starting case intake workflow")
    
    # Step 1: Normalize with LLM
    log.info("Step 1: Normalizing raw text with LLM")
    try:
        normalized = normalize_free_text_to_case(raw_text)
    except Exception as e:
        log.error(f"Normalization failed: {e}")
        raise CaseIntakeError(f"Failed to normalize text: {e}") from e
    
    # Step 2: Convert to strict payload
    log.info("Step 2: Validating and converting to DB payload")
    try:
        payload = normalized_to_case_payload(normalized)
    except Exception as e:
        log.error(f"Payload conversion failed: {e}")
        raise CaseIntakeError(f"Failed to create payload: {e}") from e
    
    # Step 3: Create or find patient
    log.info(f"Step 3: Creating/finding patient (MRN={payload.mrn})")
    try:
        patient_id = _create_or_find_patient(payload, config.api_base_url)
    except Exception as e:
        log.error(f"Patient creation failed: {e}")
        raise CaseIntakeError(f"Failed to create patient: {e}") from e
    
    # Step 4: Create encounter
    log.info(f"Step 4: Creating encounter for patient_id={patient_id}")
    try:
        encounter_id = _create_encounter(patient_id, payload, config.api_base_url)
    except Exception as e:
        log.error(f"Encounter creation failed: {e}")
        raise CaseIntakeError(f"Failed to create encounter: {e}") from e
    
    # Step 5: Create research case
    log.info(f"Step 5: Creating research case (type={payload.procedure_type})")
    try:
        research_case_id = _create_research_case(encounter_id, payload, config.api_base_url)
    except Exception as e:
        log.error(f"Research case creation failed: {e}")
        raise CaseIntakeError(f"Failed to create research case: {e}") from e
    
    log.info(f"✓ Case intake complete: patient={patient_id}, encounter={encounter_id}, case={research_case_id}")
    
    return {
        "success": True,
        "patient_id": patient_id,
        "encounter_id": encounter_id,
        "research_case_id": research_case_id,
        "procedure_type": payload.procedure_type,
        "raw_note": raw_text
    }


def _create_or_find_patient(payload: CaseCreatePayload, api_base: str) -> int:
    """Search for existing patient or create new one"""
    # Try to find existing patient
    search_response = requests.get(
        f"{api_base}/api/v1/patients/search",
        params={"q": payload.mrn}
    )
    
    # Handle search results
    if search_response.status_code == 200:
        patients = search_response.json()
        if patients:
            patient_id = patients[0]["id"]
            log.info(f"Found existing patient: ID={patient_id}, MRN={payload.mrn}")
            return patient_id
    elif search_response.status_code != 404:
        # Real error (not just "no results")
        raise CaseIntakeError(f"Patient search failed: {search_response.text}")
    
    # Create new patient
    patient_data = {
        "mrn": payload.mrn,
        "date_of_birth": str(payload.date_of_birth),
        "sex": payload.sex
    }
    
    # Only include name fields if they have values
    if payload.first_name is not None:
        patient_data["first_name"] = payload.first_name
    if payload.middle_name is not None:
        patient_data["middle_name"] = payload.middle_name
    if payload.last_name is not None:
        patient_data["last_name"] = payload.last_name
    
    create_response = requests.post(
        f"{api_base}/api/v1/patients",
        json=patient_data
    )
    
    if create_response.status_code != 201:
        raise CaseIntakeError(f"Patient creation failed: {create_response.text}")
    
    patient_id = create_response.json()["id"]
    log.info(f"Created new patient: ID={patient_id}, MRN={payload.mrn}")
    return patient_id


def _create_encounter(patient_id: int, payload: CaseCreatePayload, api_base: str) -> int:
    """Create encounter for patient"""
    encounter_data = {
        "patient_id": patient_id,
        "encounter_type": payload.encounter_type,
        "encounter_date": str(payload.encounter_date),
        "chief_complaint": payload.chief_complaint,
        "location": payload.location,
        "attending_physician": payload.attending_physician,
        "status": payload.status,
        "notes": payload.notes
    }
    
    response = requests.post(
        f"{api_base}/api/v1/encounters",
        json=encounter_data
    )
    
    if response.status_code != 201:
        raise CaseIntakeError(f"Encounter creation failed: {response.text}")
    
    encounter_id = response.json()["id"]
    log.info(f"Created encounter: ID={encounter_id}")
    return encounter_id


def _create_research_case(encounter_id: int, payload: CaseCreatePayload, api_base: str) -> int:
    """Create research case record"""
    # Map procedure type to endpoint
    endpoint_map = {
        "rotator-cuff": "rotator-cuff",
        "knee-surgical": "knee-surgical",
        "shoulder-scope": "shoulder-scope",
        "shoulder-arthroplasty": "shoulder-arthroplasty",
        "hip-scope": "hip-scope",
        "hip-arthroplasty": "hip-arthroplasty",
        "knee-arthroplasty": "knee-arthroplasty",
        "other": "other"
    }
    
    endpoint = endpoint_map.get(payload.procedure_type, "other")
    
    research_data = {
        "encounter_id": encounter_id,
        "fellow_or_pa": payload.fellow_or_pa,
        "attending": payload.attending_physician,
        "mrn": payload.mrn,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "dob": str(payload.date_of_birth),
        "surgery_date": str(payload.encounter_date),
        "laterality": payload.laterality
    }
    
    response = requests.post(
        f"{api_base}/api/v1/rc/{endpoint}",
        json=research_data
    )
    
    if response.status_code != 201:
        raise CaseIntakeError(f"Research case creation failed: {response.text}")
    
    research_case_id = response.json()["id"]
    log.info(f"Created research case: ID={research_case_id}, type={payload.procedure_type}")
    return research_case_id
