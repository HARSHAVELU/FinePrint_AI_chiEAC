export const disclaimer='FinePrint AI explains documents. It is not legal, financial, or medical advice, and it can make mistakes. Check important dates against the original document and ask a person you trust.';
export const normalize=s=>s.replace(/\s+/g,' ').trim().toLowerCase();
export function parseRows(records,name='document'){
 if(!Array.isArray(records)||!records.length)throw Error('The file must contain document rows.');
 if(records.length>400)throw Error('Maximum 400 rows. Split your document.');
 const warnings=[];
 const rows=records.map((v,i)=>{
 let r=typeof v==='string'?{text:v}:{...v};
 if(!r.text){let k=['content','paragraph','clause','body'].find(k=>r[k]);if(!k&&Object.keys(r).length===1)k=Object.keys(r)[0];if(k){r.text=r[k];warnings.push(`Used ${k} as text.`)}}
 if(typeof r.text!=='string'||!r.text.trim())throw Error(`Row ${i+1} needs text.`);
 if(r.text.length>50000)throw Error('A row is too long. Split it into paragraphs.');
 if(r.page!==undefined&&r.page!==null&&r.page!==''&&(!Number.isInteger(Number(r.page))||Number(r.page)<1))throw Error(`Row ${i+1} has an invalid page.`);
 return {doc_id:r.doc_id||name,section_id:String(r.section_id||`r${i+1}`),heading:r.heading||`Section ${i+1}`,text:r.text,page:r.page?Number(r.page):null};});
 if(new Set(rows.map(r=>r.section_id)).size!==rows.length)throw Error('Section IDs must be unique.');
 if(new Set(rows.map(r=>r.doc_id)).size!==1)throw Error('Use one doc_id per upload.');
 return {rows,warnings:[...new Set(warnings)]};
}
export function redact(rows){let count=0;const patterns=[['EMAIL',/\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b/g],['SSN',/\b\d{3}-\d{2}-\d{4}\b/g],['PHONE',/(?:\+1[ .-]?)?\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}\b/g],['ACCOUNT',/\b(?:account|claim|case)\s*(?:number|no\.?|#|:)\s*:?\s*[A-Z0-9-]{5,}/gi],['DOB',/\b(?:dob|date of birth)\s*:?\s*\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}/gi],['NAME',/\b(?:name|tenant|employee|student)\s*:\s*[A-Z][a-z]+ [A-Z][a-z]+/gi],['ADDRESS',/\b\d{1,5}\s+(?:[A-Z][a-z]+\s+){1,4}(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr)\b/g]];
 const clean=s=>{for(const [kind,re] of patterns)s=s.replace(re,()=>`[${kind}_${++count}]`);return s};
 return {rows:rows.map(r=>({...r,text:clean(r.text),heading:clean(r.heading),doc_id:clean(r.doc_id)})),count};}
const keys={housing:['rent','lease','tenant','landlord'],employment:['employee','salary','offer','employment'],school:['school','student','enrollment','iep'],insurance:['insurance','deductible','copay','claim'],benefits:['snap','medicaid','caseworker','redetermination']};
export function classify(rows){const t=rows.map(r=>r.text).join(' ').toLowerCase();const scores=Object.entries(keys).map(([f,ks])=>[f,ks.reduce((n,k)=>n+t.split(k).length-1,0)]).sort((a,b)=>b[1]-a[1]);return scores[0][1]?scores[0][0]:'other'}
const dates=/\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b/gi;
export function analyze(rows,checklists){const family=classify(rows),items=[];let id=0;
 for(const r of rows){for(const quote of r.text.split(/(?<=[.!?])\s+/)){
 if(/ignore (?:all |previous |prior )?instructions|SYSTEM:|reveal.*secret/i.test(quote))continue;
 const add=(item_type,value)=>{if(normalize(r.text).includes(normalize(quote)))items.push({id:String(++id),item_type,value,quote,section_id:r.section_id,page:r.page,heading:r.heading,badge:'High',verified:true,explanation:'Exact source passage. Confirm how it applies to you.'})};
 for(const date of quote.match(dates)||[]){const parsed=new Date(date);add('deadline',Number.isNaN(+parsed)?date:parsed.toISOString().slice(0,10))}
 for(const amount of quote.match(/\$\s*[\d,]+(?:\.\d{2})?/g)||[])add('fee',amount+(/waived|does not apply|not charged/i.test(quote)?' · waived / not charged':''));
 if(/\b(must|shall|required|submit|provide|return|bring|responsible)\b/i.test(quote))add(/penalty|terminate|responsib|landlord|employer|failure|must not|resign|notice/i.test(quote)?'obligation':'requirement',quote);
 if(/\bmeans\b|\bis defined as\b/i.test(quote))add('term',quote);
 }}
 const evidence=items.map(i=>i.quote).join(' ');
 const missing=(checklists[family]||[]).filter(c=>!c.patterns.some(p=>new RegExp(p,'i').test(evidence))).map(c=>({...c,status:'Not stated in your document'}));
 for(const r of rows)for(const type of ['deadline','fee']){const group=items.filter(i=>i.section_id===r.section_id&&i.item_type===type);if(new Set(group.map(i=>i.value)).size>1){group.forEach(i=>i.badge='Low');missing.push({key:`conflict-${r.section_id}-${type}`,status:'Needs review',question:`Section ${r.section_id} has multiple ${type} values. Which one applies to you?`})}}
 return {family,items,missing,sections:rows.map(r=>({...r,quote:r.text,mode:'extractive'}))};
}
const stop=new Set('what when where how do does is are the a an to of for in my i this document please can you me it'.split(' '));
const terms=s=>(s.toLowerCase().match(/[a-z0-9]+/g)||[]).filter(x=>!stop.has(x));
export function ask(rows,question){const q=[...new Set(terms(question))];const hits=rows.map(r=>({row:r,score:q.filter(w=>terms(r.text).includes(w)).length/Math.max(q.length,1)})).sort((a,b)=>b.score-a.score);
 if(!hits.length||hits[0].score<=.5)return {answer:'Not stated in your document. Ask the sender or the office named in your document.',abstained:true,citations:[],nearest:hits.slice(0,1).map(x=>x.row)};
 return {answer:'Your document says:',abstained:false,citations:[hits[0].row],nearest:[]};}
