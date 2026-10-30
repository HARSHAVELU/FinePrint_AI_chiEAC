from typing import TypedDict, Any
from langgraph.graph import StateGraph, START, END
from .extract import extract
from .verify import verify
from .gaps import gaps
from .simplify import simplify
class State(TypedDict,total=False):
    rows: list
    family: str
    candidates: list
    items: list
    rejected: list
    missing: list
    sections: list

def extraction(s):return {'candidates':extract(s['rows'])}
def verification(s):
    items,rejected=verify(s['candidates'],s['rows'])
    # Conflicting dates/amounts in the same section remain visible, with uncertainty.
    conflicts=[]
    for kind in ['deadline','fee']:
        for section in {i.section_id for i in items}:
            group=[i for i in items if i.item_type==kind and i.section_id==section]
            if len({i.value for i in group})>1:
                for i in group:i.badge='Low'
                conflicts.append({'status':'unclear','section_id':section,'question':f'This section has multiple {kind} values. Which applies to you?'})
    return {'items':items,'rejected':rejected+conflicts}
def gap_node(s):return {'missing':gaps(s['family'],s['items'],s['rows'])+s['rejected']}
def simplify_node(s):return {'sections':simplify(s['rows'])}
graph=StateGraph(State)
for name,fn in [('extract',extraction),('verify',verification),('gaps',gap_node),('simplify',simplify_node)]:graph.add_node(name,fn)
graph.add_edge(START,'extract');graph.add_edge('extract','verify');graph.add_edge('verify','gaps');graph.add_edge('gaps','simplify');graph.add_edge('simplify',END)
pipeline=graph.compile()

# Upload graph: every model-visible path runs redaction first.
class UploadState(TypedDict,total=False):
    content: bytes
    filename: str
    hint: str
    session_id: str
    rows: list
    warnings: list
    mapping: dict
    family: str
    index: Any

def ingest_node(s):
    from .ingest import parse_file
    rows,warnings=parse_file(s['content'],s['filename'])
    return {'rows':rows,'warnings':warnings}
def redact_node(s):
    from .redact import redact_rows
    rows,mapping=redact_rows(s['rows'])
    return {'rows':rows,'mapping':mapping}
def classify_node(s):
    from .classify import classify
    return {'family':classify(s['rows'],s.get('hint',''))}
def index_node(s):
    from .index import SessionIndex
    return {'index':SessionIndex(s['rows'],s['session_id'])}
upload_graph=StateGraph(UploadState)
for name,fn in [('ingest',ingest_node),('redact',redact_node),('classify',classify_node),('index',index_node)]:upload_graph.add_node(name,fn)
upload_graph.add_edge(START,'ingest');upload_graph.add_edge('ingest','redact');upload_graph.add_edge('redact','classify');upload_graph.add_edge('classify','index');upload_graph.add_edge('index',END)
upload_pipeline=upload_graph.compile()
