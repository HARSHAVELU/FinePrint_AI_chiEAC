import math, re
from collections import Counter
from ..config import settings
STOP=set('what when where how do does is are the a an to of for in my i this document please'.split())
def words(text):return [w for w in re.findall(r'[a-z0-9]+',text.lower()) if w not in STOP]
class SessionIndex:
    def __init__(self,rows,session_id):
        self.rows=rows;self.client=None
        if settings.retrieval=='chroma':
            import chromadb
            from sentence_transformers import SentenceTransformer
            self.encoder=SentenceTransformer('BAAI/bge-small-en-v1.5')
            self.client=chromadb.EphemeralClient()
            self.collection=self.client.create_collection(name='session-'+session_id,metadata={'hnsw:space':'cosine'})
            self.collection.add(ids=[r.section_id for r in rows],documents=[r.text for r in rows],embeddings=self.encoder.encode([r.text for r in rows],normalize_embeddings=True).tolist())
    def search(self,question,k=5):
        if self.client:
            result=self.collection.query(query_embeddings=self.encoder.encode([question],normalize_embeddings=True).tolist(),n_results=min(k,len(self.rows)))
            lookup={r.section_id:r for r in self.rows}
            return [(lookup[s],max(0,1-d)) for s,d in zip(result['ids'][0],result['distances'][0])]
        q=set(words(question));hits=[]
        for r in self.rows:
            t=set(words(r.heading+' '+r.text)); score=len(q&t)/max(1,len(q))
            hits.append((r,score))
        return sorted(hits,key=lambda x:x[1],reverse=True)[:k]
    def close(self):
        if self.client:self.client.delete_collection(self.collection.name)
        self.rows=[]
