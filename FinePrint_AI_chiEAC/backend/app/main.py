import asyncio, secrets, time, os
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .schemas import SessionRequest, AskRequest, SearchRequest
from .graph.ingest import parse_file
from .graph.redact import redact_rows
from .graph.classify import classify
from .graph.index import SessionIndex
from .graph.pipeline import pipeline, upload_pipeline
from .graph.answer import answer
sessions={};limits={};semaphore=asyncio.Semaphore(2)
def purge():
    now=time.monotonic()
    for sid in list(sessions):
        if now-sessions[sid]['touched']>settings.ttl:
            sessions.pop(sid)['index'].close()
    for ip in list(limits):
        if not limits[ip] or now-limits[ip][-1]>60:limits.pop(ip,None)
async def cleaner():
    while True:
        await asyncio.sleep(15);purge()
@asynccontextmanager
async def lifespan(app):
    task=asyncio.create_task(cleaner())
    yield
    task.cancel()
    for s in sessions.values():s['index'].close()
    sessions.clear()
app=FastAPI(title='FinePrint AI',version='0.1.0',lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=os.getenv('FINEPRINT_ORIGINS','http://localhost:5173').split(','),allow_methods=['GET','POST','DELETE'],allow_headers=['Content-Type'])
@app.middleware('http')
async def guards(request,call_next):
    purge();ip=request.client.host if request.client else 'unknown';now=time.monotonic()
    bucket=limits.setdefault(ip,deque())
    while bucket and now-bucket[0]>60:bucket.popleft()
    if len(bucket)>=30:return JSONResponse({'error':'rate_limited','message':'Please wait one minute and try again.'},status_code=429)
    bucket.append(now)
    if int(request.headers.get('content-length','0'))>settings.max_bytes+65536:return JSONResponse({'error':'file_too_large','message':'Maximum file size is 5 MB.'},status_code=413)
    response=await call_next(request)
    response.headers['Cache-Control']='no-store';response.headers['X-Content-Type-Options']='nosniff'
    return response
@app.exception_handler(ValueError)
async def invalid(request,exc):
    message='Invalid document fields. Check text, section_id, doc_id, and page.' if isinstance(exc,ValidationError) else str(exc)
    return JSONResponse({'error':'invalid_input','message':message},status_code=422)
@app.exception_handler(RequestValidationError)
async def invalid_request(request,exc):return JSONResponse({'error':'invalid_request','message':'Check required fields and allowed lengths.'},status_code=422)
@app.exception_handler(Exception)
async def unexpected(request,exc):return JSONResponse({'error':'processing_failed','message':'Could not process this document. Check the input or try again.'},status_code=500)
def session(sid):
    purge()
    if sid not in sessions:raise HTTPException(404,'Session ended. Please upload again.')
    s=sessions[sid];s['touched']=time.monotonic();return s
@app.get('/health')
def health():return {'status':'ok','mode':settings.mode,'retrieval':settings.retrieval,'redaction':settings.redaction}
@app.post('/upload')
async def upload(file:UploadFile=File(...),family_hint:str=Form('')):
    content=await file.read(settings.max_bytes+1)
    if len(sessions)>=100:raise HTTPException(503,'Server is busy. Try again shortly.')
    sid=secrets.token_urlsafe(32)
    async with semaphore:
        result=await asyncio.to_thread(upload_pipeline.invoke,{'content':content,'filename':file.filename or '', 'hint':family_hint[:50], 'session_id':sid})
    rows=result['rows'];mapping=result['mapping'];warnings=result['warnings']
    s={'rows':rows,'mapping':mapping,'index':result['index'],'family':result['family'],'touched':time.monotonic()}
    sessions[sid]=s
    # PII mapping stays only in this session's memory. Return only typed placeholders by default.
    return {'session_id':sid,'family':s['family'],'rows':[r.model_dump() for r in rows],'redacted_count':len(mapping),'warnings':warnings,'mode':settings.mode}
@app.post('/search')
def search(req:SearchRequest):return {'hits':[{'row':r.model_dump(),'score':score} for r,score in session(req.session_id)['index'].search(req.question)]}
@app.post('/analyze')
async def analyze(req:SessionRequest):
    s=session(req.session_id)
    if 'result' not in s:
        async with semaphore:
            # Thread is allowed to finish after timeout; no retry that duplicates model calls.
            try:s['result']=await asyncio.wait_for(asyncio.to_thread(pipeline.invoke,{'rows':s['rows'],'family':s['family']}),timeout=180)
            except asyncio.TimeoutError:raise HTTPException(504,'Analysis timed out. Use a shorter document.')
    r=s['result']
    return {'family':s['family'],'mode':settings.mode,'items':[i.model_dump() for i in r['items']],'missing':r['missing'],'sections':r['sections']}
@app.post('/ask')
async def ask(req:AskRequest):
    async with semaphore:return await asyncio.to_thread(answer,session(req.session_id),req.question)
@app.delete('/session/{session_id}')
def close(session_id:str):
    s=sessions.pop(session_id,None)
    if s:s['index'].close()
    return {'deleted':True}
