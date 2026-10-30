import json,re
from pathlib import Path

def gaps(family, items, rows):
    path=Path(__file__).resolve().parents[1]/'checklists'/f'{family}.json'
    if not path.exists():return [{'status':'not stated in your document','question':'What type of document is this? Ask the sender to explain its purpose.'}]
    # Only verified passages count as evidence, never model labels alone.
    evidence=' '.join(i.quote.lower() for i in items if i.verified)
    return [{'key':c['key'],'status':'not stated in your document','question':c['question']} for c in json.loads(path.read_text()) if not any(re.search(p,evidence,re.I) for p in c['patterns'])]
