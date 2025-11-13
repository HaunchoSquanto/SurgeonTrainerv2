"""
Add a real patient case to the database.
Interactive terminal prompt for pasting surgical notes.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from services.case_intake import create_case_from_raw, CaseIntakeError

if __name__ == "__main__":
    print("=" * 70)
    print("Add Patient Case to Database")
    print("=" * 70)
    print("\nPaste your surgical note below.")
    print("When finished, press Enter, then Ctrl+Z (Windows) or Ctrl+D (Mac/Linux), then Enter again.")
    print("-" * 70)
    
    # Read multi-line input from terminal
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    
    RAW_NOTE = "\n".join(lines).strip()
    
    if not RAW_NOTE:
        print("\n✗ No input provided. Aborted.")
        sys.exit(0)
    
    print("\n" + "=" * 70)
    print("Review Your Input:")
    print("=" * 70)
    print(RAW_NOTE)
    print("-" * 70)
    
    # Confirm before proceeding
    response = input("\nAdd this case to the database? (yes/no): ")
    if response.lower() != "yes":
        print("Aborted.")
        sys.exit(0)
    
    try:
        print("\n[Step 1] Normalizing with Studio LM...")
        result = create_case_from_raw(RAW_NOTE)
        
        print("\n" + "=" * 70)
        print("✓✓ SUCCESS!")
        print("=" * 70)
        print(f"Patient ID:       {result['patient_id']}")
        print(f"Encounter ID:     {result['encounter_id']}")
        print(f"Research Case ID: {result['research_case_id']}")
        print(f"Procedure Type:   {result['procedure_type']}")
        print("\nCase successfully added to database!")
        
    except CaseIntakeError as e:
        error_msg = str(e)
        
        # Check if MRN is missing
        if "mrn" in error_msg.lower() or "medical record" in error_msg.lower():
            print("\n⚠️  Missing MRN - Please provide the Medical Record Number")
            mrn = input("Enter MRN: ").strip()
            
            if mrn:
                # Retry with MRN added to note
                RAW_NOTE_WITH_MRN = f"MRN: {mrn}\n{RAW_NOTE}"
                try:
                    print("\n[Retrying] Normalizing with MRN...")
                    result = create_case_from_raw(RAW_NOTE_WITH_MRN)
                    
                    print("\n" + "=" * 70)
                    print("✓✓ SUCCESS!")
                    print("=" * 70)
                    print(f"Patient ID:       {result['patient_id']}")
                    print(f"Encounter ID:     {result['encounter_id']}")
                    print(f"Research Case ID: {result['research_case_id']}")
                    print(f"Procedure Type:   {result['procedure_type']}")
                    print("\nCase successfully added to database!")
                    sys.exit(0)
                except Exception as retry_e:
                    print(f"\n✗ Retry failed: {retry_e}")
                    sys.exit(1)
        
        print("\n" + "=" * 70)
        print("✗ CASE INTAKE ERROR")
        print("=" * 70)
        print(f"{e}")
        sys.exit(1)
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ UNEXPECTED ERROR")
        print("=" * 70)
        print(f"{type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
