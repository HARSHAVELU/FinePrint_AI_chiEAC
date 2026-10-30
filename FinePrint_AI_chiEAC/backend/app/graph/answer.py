from ..config import settings
from ..schemas import CandidateList
from .model import call_model
from .verify import verify

def answer(session, question):
    hits=session['index'].search(question,5)
    nearest=[{'section_id':r.section_id,'quote':r.text,'score':score,'page':r.page} for r,score in hits[:3]]
    abstain={'answer':'Not stated in your document. Ask the sender or the office named in your document.','abstained':True,'citations':[],'nearest':nearest}
    if not hits or all(s<settings.threshold for _,s in hits[:3]):return abstain
    if settings.mode=='demo':
        # Only return passages with substantive query overlap; no inferred answers.
        r,score=hits[0]
        from .index import words
        query=set(words(question));overlap=query & set(words(r.text))
        if not overlap or score<=.5:return abstain
        return {'answer':'Your document says: '+r.text,'abstained':False,'citations':[{'section_id':r.section_id,'quote':r.text,'page':r.page,'badge':'High'}],'nearest':nearest}
    candidates=CandidateList.model_validate(call_model('answer',{'question':question,'passages':[r.model_dump() for r,_ in hits]}))
    valid,_=verify(candidates.items,session['rows'],hits[0][1])
    if not valid:return abstain
    return {'answer':'\n'.join(i.value for i in valid),'abstained':False,'citations':[i.model_dump() for i in valid],'nearest':nearest}
