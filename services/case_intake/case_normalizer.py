"""
Case normalization using Studio LM.
Converts raw surgical text into structured NormalizedCase schema.
"""
from pydantic import ValidationError
from services.common import call_studio_lm, get_logger
from .schemas import NormalizedCase
import json

log = get_logger(__name__)

SYSTEM_PROMPT = """
You convert messy surgical dictation into strict JSON for a surgical case logging system.
Output ONLY valid JSON matching this schema. Extract as much as possible from the text.

REQUIRED FIELDS (must extract these):
- mrn: Medical record number (string)
- date_of_birth: YYYY-MM-DD format (string). Calculate from age and current date if needed
- sex: "M", "F", or "O" (string). Use "M" for male, "F" for female
- surgery_date: YYYY-MM-DD format (string). Convert MM/DD/YY to YYYY-MM-DD if needed
- procedure_type: Choose from: "rotator-cuff", "knee-surgical", "shoulder-scope", "shoulder-arthroplasty", "hip-scope", "hip-arthroplasty", "knee-arthroplasty", "other" (string)

OPTIONAL FIELDS:
- first_name: Patient first name (string or null)
- last_name: Patient last name (string or null)
- middle_name: string or null
- laterality: "Right", "Left", or "Bilateral" or null
- attending: Attending surgeon name or null
- fellow_or_pa: Fellow or PA name or null
- chief_complaint: Why patient came in or null
- location: Facility/hospital name or null
- notes: Any additional clinical notes or null

Output JSON format:
{{
  "mrn": "string (required)",
  "first_name": "string or null",
  "last_name": "string or null",
  "middle_name": "string or null",
  "date_of_birth": "YYYY-MM-DD (required)",
  "sex": "M/F/O (required)",
  "surgery_date": "YYYY-MM-DD (required)",
  "procedure_type": "one of the procedure types above (required)",
  "laterality": "Right/Left/Bilateral or null",
  "attending": "string or null",
  "fellow_or_pa": "string or null",
  "chief_complaint": "string or null",
  "location": "string or null",
  "notes": "string or null"
}}
"""

def normalize_free_text_to_case(raw_text: str) -> NormalizedCase:
    """
    Normalize free text surgical notes into structured NormalizedCase.
    
    Args:
        raw_text: Raw surgical dictation or note text
    
    Returns:
        NormalizedCase with extracted data
    
    Raises:
        ValueError: If LLM returns invalid JSON or Pydantic validation fails
    """
    log.info(f"Normalizing text: {len(raw_text)} chars")
    
    user_prompt = f"""
    Text:
    \"\"\"{raw_text}\"\"\"

    Extract the case information into the JSON format specified.
    If a field is unknown or not mentioned, use null.
    Ensure all required fields are present.
    """
    
    try:
        llm_output = call_studio_lm(user_prompt=user_prompt, system_prompt=SYSTEM_PROMPT)
    except Exception as e:
        log.error(f"LLM call failed: {e}")
        raise ValueError(f"Failed to call LLM: {e}") from e

    # Parse LLM output as JSON
    try:
        data = json.loads(llm_output)
    except json.JSONDecodeError as e:
        log.error(f"Invalid JSON from LLM: {llm_output[:200]}...")
        raise ValueError(f"LLM returned invalid JSON: {e}. Output was: {llm_output}") from e

    # Store original note for reference
    data["raw_note"] = raw_text
    
    # Validate with Pydantic
    try:
        normalized = NormalizedCase(**data)
        log.info(f"Successfully normalized case: MRN={normalized.mrn}, procedure={normalized.procedure_type}")
        return normalized
    except ValidationError as e:
        log.error(f"Pydantic validation failed: {e}")
        raise ValueError(f"Normalization validation failed: {e}") from e
