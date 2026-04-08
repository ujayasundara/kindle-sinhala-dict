import json
import os
import sys
from convert import sinhala_to_singlish

# Load the local JSON file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "en_to_si.json")

def validate_all_meanings():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found.")
        return

    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"Validating {len(data)} entries...")
    
    # Regex to detect any Sinhala character (U+0D80 to U+0DFF)
    # This will check if any Sinhala character remains in the Singlish output
    import re
    sinhala_range = re.compile(r'[\u0D80-\u0DFF]')
    
    failures = []
    
    for i, entry in enumerate(data):
        for word, meaning in entry.items():
            singlish = sinhala_to_singlish(meaning)
            
            # Find any untransliterated Sinhala characters in the Singlish result
            mismatches = sinhala_range.findall(singlish)
            if mismatches:
                failures.append({
                    "word": word,
                    "sinhala": meaning,
                    "singlish": singlish,
                    "failed_chars": "".join(set(mismatches))
                })

    if failures:
        print(f"\nFound {len(failures)} problematic transliterations:")
        # Print top 20 failures
        for f in failures[:20]:
            print(f"- {f['word']}: '{f['sinhala']}' -> '{f['singlish']}' (Failed chars: {f['failed_chars']})")
        
        if len(failures) > 20:
            print(f"... and {len(failures) - 20} more.")
            
        # Summary of unique failed characters
        all_failed_chars = set()
        for f in failures:
            for char in f['failed_chars']:
                all_failed_chars.add(char)
        print(f"\nSUMMARY: You need to add rules for these characters: {' '.join(all_failed_chars)}")
    else:
        print("\nSUCCESS! All Sinhala characters were successfully transliterated.")

if __name__ == "__main__":
    validate_all_meanings()
