import json,csv
from pathlib import Path
from openpyxl import Workbook
ROOT=Path(__file__).resolve().parents[1]
checks={
'housing':[('rent','rent','What is the rent amount and due date?'),('late_fee','late fee','What late fee and grace period apply?'),('deposit','deposit','When and how is the deposit returned?'),('dates','lease.*(start|end)|begins','When does the lease start and end?'),('renewal','renew','Does the lease renew automatically?'),('notice','notice','How much notice must each party give?'),('utilities','utilit','Who pays each utility?'),('repairs','repair','How do I report a repair?'),('pets','pet','What are the pet and guest rules?'),('entry','enter|entry','What notice is required before entry?')],
'employment':[('start','start|begins','What is my start date and location?'),('pay','salary|pay rate','What is the pay rate and frequency?'),('overtime','overtime|nonexempt','Am I eligible for overtime?'),('at_will','at.will','What are the employment terms?'),('benefits','benefits','When do benefits begin?'),('pto','paid time|pto','How does paid time off accrue?'),('notice','resign|termination|notice','What notice is required?'),('sign','sign|return','When must I accept the offer?')],
'school':[('deadline','due|deadline|return','When must I respond?'),('documents','documents|proof','What documents do I need?'),('meeting','meeting','When and where is the meeting?'),('contact','contact|office','Who can answer questions?'),('appeal','appeal|dispute','How can I dispute the decision?'),('language','interpreter|language','Can I request an interpreter?'),('cost','fee|cost','What costs apply?'),('reschedule','reschedule','How can I reschedule?')],
'insurance':[('deductible','deductible','What is my deductible?'),('maximum','out.of.pocket','What is my out-of-pocket maximum?'),('copay','copay|coinsurance','What copays apply?'),('network','network','What are the network rules?'),('authorization','prior authorization','Is prior authorization required?'),('billed','billed|owe','How much do I owe?'),('appeal','appeal','How and when do I appeal?'),('contact','contact|call','Who should I contact?')],
'benefits':[('action','submit|return','What action must I take?'),('deadline','due|deadline|before','What is the deadline?'),('documents','documents|proof','What documents do I need?'),('method','upload|mail|fax','How do I submit them?'),('consequence','close|stop|failure','What happens if I do not reply?'),('appeal','appeal|hearing','How can I request a hearing?'),('continue','continue','Do benefits continue during appeal?'),('contact','caseworker|contact','Who is my contact?'),('language','language|interpreter','Is language help available?')]}
for family,entries in checks.items():
 (ROOT/f'backend/app/checklists/{family}.json').write_text(json.dumps([{'key':k,'patterns':[p],'question':q} for k,p,q in entries],indent=2))
fixtures={
'housing': [('Rent','Rent of $1,200 is due on November 5, 2026.'),('Deposit','Tenant must pay a security deposit of $800 before move-in.'),('Notice','Tenant must give 30 days written notice to end the lease.'),('Repairs','The landlord is responsible for repairs. Report problems to the office.'),('Late fee','A late fee of $45 applies after the grace period.'),('Terms','Security deposit means money held to cover unpaid rent or damage.'),('Required records','Tenant must provide proof of income by November 2, 2026.')],
'employment':[('Start','Employment begins on November 16, 2026.'),('Salary','The pay rate is $25 per hour.'),('Acceptance','You must sign and return the offer by November 6, 2026.'),('Benefits','You must submit benefits forms by November 20, 2026.'),('Notice','Employees must give two weeks notice before resigning.'),('Terms','Nonexempt means eligible for overtime pay under this offer.'),('Fee','The training fee of $50 is waived and will not be charged.')],
'school':[('Response','You must return the school enrollment form by November 4, 2026.'),('Documents','The student must provide proof of address and an immunization record.'),('Meeting','The school meeting is on November 10, 2026 at 3 p.m. in Room 2.'),('Fee','The school activity fee is $20.'),('Language','You may ask the office for an interpreter.'),('Terms','Enrollment means signing up for school.'),('Contact','You must contact the school office to reschedule the meeting.')],
'insurance':[('Appeal','You must submit an appeal by December 1, 2026.'),('Cost','The annual deductible is $500.'),('Copay','The office visit copay is $25.'),('Network','You must use network providers for the stated copay.'),('Authorization','You must obtain prior authorization before the procedure.'),('Terms','Deductible means the amount you pay before the plan pays for covered care.'),('Contact','You must call the plan office for help with a claim.')],
'benefits':[('Deadline','You must return the SNAP redetermination form by November 12, 2026.'),('Documents','You must submit proof of income and proof of address.'),('Method','You must upload the documents through the benefits portal.'),('Consequence','Failure to respond will close the benefits case.'),('Appeal','You must request a fair hearing by December 2, 2026.'),('Terms','Redetermination means a review of whether you still qualify.'),('Contact','You must contact your caseworker if you need help.')]
}
labels=[];docs=[]
for family,clauses in fixtures.items():
 for variant in range(1,7):
  docid=f'{family}-{variant:02}'
  rows=[dict(doc_id=docid,section_id=str(i+1),heading=h,text=t.replace('$1,200',f'${1200+variant*10:,}'),page=i//4+1,source_file='synthetic-example') for i,(h,t) in enumerate(clauses)]
  (ROOT/f'data/golden/docs/{docid}.json').write_text(json.dumps(rows,indent=2));docs.append({'id':docid,'family':family,'rows':rows,'synthetic':True})
  # Labels are authored independently from the extractor: explicit expected facts.
  facts={
   'housing': [('deadline','2026-11-05','1'),('fee',f'${1200+variant*10:,}','1'),('fee','$800','2'),('fee','$45','5'),('deadline','2026-11-02','7'),('requirement',rows[1]['text'],'2'),('obligation',rows[2]['text'],'3'),('term',rows[5]['text'],'6')],
   'employment':[('deadline','2026-11-16','1'),('fee','$25','2'),('deadline','2026-11-06','3'),('deadline','2026-11-20','4'),('requirement',rows[2]['text'],'3'),('obligation',rows[4]['text'],'5'),('term',rows[5]['text'],'6'),('fee','$50 (waived / not charged)','7')],
   'school':[('deadline','2026-11-04','1'),('deadline','2026-11-10','3'),('fee','$20','4'),('requirement',rows[1]['text'],'2'),('requirement',rows[0]['text'],'1'),('term',rows[5]['text'],'6')],
   'insurance':[('deadline','2026-12-01','1'),('fee','$500','2'),('fee','$25','3'),('requirement',rows[0]['text'],'1'),('requirement',rows[4]['text'],'5'),('term',rows[5]['text'],'6')],
   'benefits':[('deadline','2026-11-12','1'),('deadline','2026-12-02','5'),('requirement',rows[0]['text'],'1'),('requirement',rows[1]['text'],'2'),('requirement',rows[2]['text'],'3'),('term',rows[5]['text'],'6')]
  }[family]
  for kind,value,section in facts:labels.append(dict(doc_id=docid,item_type=kind,value=value,section_id=section,quote=rows[int(section)-1]['text'],ambiguous=False,notes='Single-pass authored synthetic fixture; independent human reconciliation pending.'))
with (ROOT/'data/golden/labels.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(labels[0]));w.writeheader();w.writerows(labels)
(ROOT/'frontend/src/demos.json').write_text(json.dumps([docs[0],docs[6],docs[24]],indent=2))
(ROOT/'data/golden/SOURCES.md').write_text('# Corpus provenance\n\nAll 30 current documents are synthetic fixtures authored for this implementation. They are six closely related variants per family, not the required public/synthetic mix. They are not evidence of generalization. No public source has been downloaded or represented as collected.\n\nRequired before Gate 4: replace 15 fixtures with public documents, record exact URLs and retrieval dates, complete a second labeling pass on a different day, reconcile disagreements, and reach about 300 labels.\n')
(ROOT/'data/golden/SOURCES.md').open('a').write('# Golden set status\n\n30 synthetic documents; '+str(len(labels))+' single-pass expected facts. No real personal data. These are smoke-test fixtures, not the completed golden set. `python scripts/seed.py` reproduces them. Do not use smoke scores in resume claims.\n')
# downloadable input templates
p=ROOT/'public/templates';p.mkdir(parents=True,exist_ok=True)
rows=docs[0]['rows'];(p/'fineprint-template.json').write_text(json.dumps(rows,indent=2))
with (p/'fineprint-template.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
w=Workbook();s=w.active;s.append(list(rows[0]));
for r in rows:s.append(list(r.values()))
w.save(p/'fineprint-template.xlsx')
