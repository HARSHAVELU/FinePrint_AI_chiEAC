import re
from rapidfuzz import fuzz
from ..schemas import Item

def norm(s): return re.sub(r'\s+', ' ', s).strip().casefold()
def verify(items, rows, retrieval_score=1.0):
    lookup={r.section_id:r for r in rows}; valid=[]; rejected=[]
    for item in items:
        row=lookup.get(item.section_id)
        exact=bool(row and norm(item.quote) in norm(row.text))
        fuzzy=bool(row and len(item.quote)>=24 and fuzz.partial_ratio(norm(item.quote),norm(row.text))>=95)
        if not exact and not fuzzy:
            rejected.append({'status':'possibly mentioned, could not verify','section_id':item.section_id,'question':'Check the original passage before relying on this item.'})
            continue
        # Fuzzy quotes are replaced with a real source span so main panels always display original text.
        if not exact: item.quote=row.text
        item.verified=True; item.match='exact' if exact else 'fuzzy'
        item.badge='Low' if not exact or item.confidence<.65 else ('Medium' if item.inference or retrieval_score<.18 else 'High')
        valid.append(item)
    return valid,rejected
