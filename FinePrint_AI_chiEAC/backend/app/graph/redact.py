import re
from ..config import settings
PATTERNS = {
 'EMAIL': r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b',
 'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
 'PHONE': r'(?<!\w)(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b',
 'ACCOUNT': r'(?i)\b(?:account|claim|case)\s*(?:number|no\.?|#|:)\s*:?\s*[A-Z0-9-]{5,}',
 'DOB': r'(?i)\b(?:date of birth|dob)\s*:?\s*\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}',
 'ADDRESS': r'\b\d{1,5}\s+(?:[A-Z][a-z]+\s+){1,4}(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr)\b',
 'NAME': r'(?i)\b(?:name|tenant|employee|student|applicant)\s*:\s*[A-Z][a-z]+ [A-Z][a-z]+'
}
def redact_rows(rows):
    mapping = {}
    analyzer = None
    if settings.redaction == 'presidio':
        from presidio_analyzer import AnalyzerEngine
        analyzer = AnalyzerEngine()
    def replace(text):
        spans = []
        for kind, pattern in PATTERNS.items():
            spans.extend((m.start(), m.end(), kind) for m in re.finditer(pattern, text))
        if analyzer:
            spans += [(x.start,x.end,x.entity_type) for x in analyzer.analyze(text=text, language='en', entities=['PERSON','EMAIL_ADDRESS','PHONE_NUMBER','US_SSN','LOCATION','DATE_TIME']) if x.entity_type != 'DATE_TIME']
        accepted=[]
        for start,end,kind in sorted(spans,key=lambda x: (x[0],-(x[1]-x[0]))):
            if not accepted or start >= accepted[-1][1]: accepted.append((start,end,kind))
        for start,end,kind in reversed(accepted):
            original=text[start:end]
            key=next((k for k,v in mapping.items() if v==original),None)
            if key is None:
                key=f'[{kind}_{len(mapping)+1}]'; mapping[key]=original
            text=text[:start]+key+text[end:]
        return text
    redacted = [r.model_copy(update={k:replace(getattr(r,k)) for k in ['text','heading','source_file','doc_id']}) for r in rows]
    return redacted, mapping
