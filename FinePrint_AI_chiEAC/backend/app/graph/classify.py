from ..config import settings
from .model import call_model
KEYWORDS={'housing':['tenant','lease','landlord','rent','deposit'],'employment':['employee','offer','salary','employer','payroll'],'school':['student','school','enroll','iep','tuition'],'insurance':['claim','copay','deductible','insurer','coverage'],'benefits':['snap','medicaid','caseworker','redetermination','benefits case']}
def classify(rows, hint=''):
    if settings.mode=='llm':
        result=call_model('classify',{'rows':[r.model_dump() for r in rows],'hint':hint})
        family=result.get('family','other')
        return family if family in KEYWORDS else 'other'
    text=' '.join(r.text.lower() for r in rows)
    scores={f:sum(text.count(k) for k in ks) for f,ks in KEYWORDS.items()}
    best=max(scores,key=scores.get)
    return best if scores[best]>0 else 'other'
