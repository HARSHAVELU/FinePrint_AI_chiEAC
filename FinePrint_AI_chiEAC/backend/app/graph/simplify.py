import textstat
from ..config import settings
from .model import call_model
from .verify import norm

def simplify(rows):
    result=[]
    for r in rows:
        # Demo mode is an extractive reading aid, not an unmeasured AI paraphrase.
        text=r.text;quote=r.text;attempts=0
        if settings.mode=='llm':
            for attempt in range(3):
                candidate=call_model('simplify',{'text':r.text,'section_id':r.section_id,'maximum_grade':8,'retry':attempt})
                text=candidate['text'];quote=candidate['quote'];attempts=attempt
                if not norm(quote) or norm(quote) not in norm(r.text):text=r.text;quote=r.text
                if textstat.flesch_kincaid_grade(text)<=8:break
        grade=textstat.flesch_kincaid_grade(text)
        result.append({'section_id':r.section_id,'text':text,'quote':quote,'grade':grade,'flagged':grade>8,'retries':attempts,'badge':'Low' if grade>8 else 'High','mode':'extractive' if settings.mode=='demo' else 'generated'})
    return result
