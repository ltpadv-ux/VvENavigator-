"""Enterprise 11.9 Governance Policy Baseline & Strategic Doctrine Register."""
from __future__ import annotations
from hashlib import sha256
from typing import Any
ENGINE_VERSION='11.9.0'

def _id(prefix:str,*parts:Any)->str:
    return f"{prefix}-"+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def build_policy_baseline_and_doctrine(drift_result:dict[str,Any], consistency_history:list[dict[str,Any]]|dict[str,Any], context:dict[str,Any]|None=None, existing:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; existing=existing or {}
    records=consistency_history.get('records',[]) if isinstance(consistency_history,dict) else (consistency_history or [])
    if len(records)<3:
        return {'governance_policy_baseline_doctrine_version':ENGINE_VERSION,'status':'ONVOLDOENDE HISTORIE VOOR DOCTRINE','doctrines':[],'automatic_policy_change':False}
    grouped={}
    for r in records:
        topic=str(r.get('topic',r.get('domain','algemeen')))
        grouped.setdefault(topic,[]).append(r)
    doctrines=[]
    prior={d.get('topic'):d for d in existing.get('doctrines',[]) or []}
    for topic,items in grouped.items():
        decisions=[str(x.get('decision',x.get('current_intervention',''))).strip() for x in items if str(x.get('decision',x.get('current_intervention',''))).strip()]
        if not decisions: continue
        dominant=max(set(decisions),key=decisions.count)
        same_count=sum(1 for x in items if bool(x.get('same_course',not x.get('material_divergence',False))))
        rationale_count=sum(1 for x in items if bool(x.get('board_rationale_complete',True)))
        confidence=round((same_count/len(items)*0.6+rationale_count/len(items)*0.4)*100,1)
        old=prior.get(topic,{})
        doctrine_id=old.get('doctrine_id') or _id('GOVDOC',topic,dominant)
        principle=context.get('principles',{}).get(topic) if isinstance(context.get('principles'),dict) else None
        doctrines.append({'doctrine_id':doctrine_id,'topic':topic,'strategic_principle':principle or f"Volg als voorkeurslijn: {dominant}, tenzij actuele feiten of expliciet gemotiveerde beleidsontwikkeling anders vereisen.",'dominant_course':dominant,'supporting_decisions':len(items),'consistency_confidence':confidence,'status':'CONCEPT DOCTRINE','human_approval_required':True,'source_policy_status':drift_result.get('status','ONBEKEND')})
    doctrines.sort(key=lambda x:(x['consistency_confidence'],x['supporting_decisions']),reverse=True)
    baseline_id=existing.get('baseline_id') or _id('GOVBASE',len(doctrines),drift_result.get('status',''))
    return {'governance_policy_baseline_doctrine_version':ENGINE_VERSION,'status':'BELEIDSBASELINE & DOCTRINE GEREED' if doctrines else 'GEEN DOCTRINE AFLEIDBAAR','baseline_id':baseline_id,'policy_status':drift_result.get('status','ONBEKEND'),'doctrine_count':len(doctrines),'doctrines':doctrines,'human_policy_approval_required':True,'human_legal_governance_review_required':True,'automatic_policy_change':False,'automatic_decision':False,'next_action':'Laat Bestuur/ALV de concept-doctrines expliciet vaststellen, wijzigen of verwerpen.'}
