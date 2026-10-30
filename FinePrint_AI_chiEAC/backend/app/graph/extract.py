import re
from datetime import datetime, timedelta
from ..schemas import Item, CandidateList
from ..config import settings
from .model import call_model
MONTHS='January February March April May June July August September October November December'.split()
DATE_RE=r'\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|(?:'+'|'.join(MONTHS)+r')\s+\d{1,2},?\s+\d{4})\b'
def normalize_date(s):
    for fmt in ['%Y-%m-%d','%m/%d/%Y','%B %d, %Y','%B %d %Y']:
        try:return datetime.strptime(s,fmt).date().isoformat()
        except ValueError:pass
    return s
def demo_extract(rows):
    items=[]
    for r in rows:
        for sentence in re.split(r'(?<=[.!?])\s+',r.text):
            if re.search(r'(?i)ignore (?:all |previous |prior )?instructions|SYSTEM:|reveal.*secret',sentence):continue
            base=dict(section_id=r.section_id,quote=sentence,confidence=.8,explanation='Source text shown below. Demo extraction; check the original.')
            for date in re.findall(DATE_RE,sentence,re.I):
                items.append(Item(item_type='deadline',value=normalize_date(date),**base))
            for fee in re.findall(r'\$\s*[\d,]+(?:\.\d{2})?',sentence):
                waived=bool(re.search(r'(?i)waived|does not apply|no .*fee|not charged',sentence))
                items.append(Item(item_type='fee',value=fee.replace(' ','')+(' (waived / not charged)' if waived else ''),**base))
            if re.search(r'(?i)\b(?:must|shall|required|submit|provide|return|bring|responsible)\b',sentence):
                kind='obligation' if re.search(r'(?i)penalty|terminate|responsib|landlord|employer|failure|must not|resign|notice',sentence) else 'requirement'
                items.append(Item(item_type=kind,value=sentence,**base))
            if re.search(r'(?i)\bmeans\b|\bis defined as\b',sentence):items.append(Item(item_type='term',value=sentence,**base))
    from .dates import relative_deadlines
    return items+relative_deadlines(rows)

def extract(rows):
    if settings.mode == 'demo':return demo_extract(rows)
    items=[]
    for kind in ['deadline','requirement','fee','obligation','term','missing']:
        result=CandidateList.model_validate(call_model('extract_'+kind, [r.model_dump() for r in rows]))
        if any(x.item_type!=kind for x in result.items):raise ValueError('Model returned an unexpected item type.')
        items.extend(result.items)
    return items
