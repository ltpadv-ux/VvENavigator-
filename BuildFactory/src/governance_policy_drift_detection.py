"""Enterprise 11.8 Governance Consistency History & Policy Drift Detection."""
from __future__ import annotations
from statistics import mean
from typing import Any
ENGINE_VERSION='11.8.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def analyze_policy_drift(history:list[dict[str,Any]]|dict[str,Any], window:int=5, drift_threshold:float=35.0)->dict[str,Any]:
    records=history.get('records',[]) if isinstance(history,dict) else (history or [])
    normalized=[]
    for r in records:
        normalized.append({'date':r.get('date',r.get('meeting_date','')),'topic':r.get('topic',r.get('domain','algemeen')),'same_course':bool(r.get('same_course',not r.get('material_divergence',False))),'divergence_score':_num(r.get('divergence_score',r.get('best_precedent',{}).get('divergence_score',0))),'material_divergence':bool(r.get('material_divergence',False)),'rationale_complete':bool(r.get('board_rationale_complete',True)),'decision':r.get('decision',r.get('current_intervention',''))})
    if len(normalized)<3:
        return {'governance_policy_drift_detection_version':ENGINE_VERSION,'status':'ONVOLDOENDE HISTORIE','record_count':len(normalized),'alerts':[],'automatic_policy_change':False}
    recent=normalized[-max(3,window):]
    avg_div=round(mean(x['divergence_score'] for x in recent),1)
    material_share=round(sum(1 for x in recent if x['material_divergence'])/len(recent)*100,1)
    unexplained=sum(1 for x in recent if x['material_divergence'] and not x['rationale_complete'])
    trend=[]
    for i in range(1,len(recent)):
        trend.append(recent[i]['divergence_score']-recent[i-1]['divergence_score'])
    slope=round(mean(trend),1) if trend else 0.0
    drift=avg_div>=drift_threshold or material_share>=50 or (slope>=10 and avg_div>=20)
    conscious=drift and unexplained==0
    status='BEWUSTE BELEIDSONTWIKKELING' if conscious else ('POLICY DRIFT - REVIEW VEREIST' if drift else 'BELEID CONSISTENT')
    alerts=[]
    if avg_div>=drift_threshold: alerts.append({'severity':'ORANJE','type':'AVERAGE_DIVERGENCE','message':'Gemiddelde beleidsafwijking ligt boven de ingestelde grens.'})
    if material_share>=50: alerts.append({'severity':'ORANJE','type':'MATERIAL_DIVERGENCE_SHARE','message':'Minstens de helft van recente besluiten wijkt materieel af van precedent.'})
    if unexplained>0: alerts.append({'severity':'ROOD','type':'UNEXPLAINED_DRIFT','message':'Materiële beleidsafwijkingen zonder vastgelegde motivering gevonden.'})
    topics={}
    for x in recent:
        topics.setdefault(x['topic'],[]).append(x['divergence_score'])
    topic_drift=[{'topic':k,'avg_divergence':round(mean(v),1),'record_count':len(v)} for k,v in topics.items()]
    topic_drift.sort(key=lambda x:x['avg_divergence'],reverse=True)
    return {'governance_policy_drift_detection_version':ENGINE_VERSION,'status':status,'record_count':len(normalized),'window_size':len(recent),'average_divergence':avg_div,'material_divergence_share_pct':material_share,'drift_slope':slope,'unexplained_material_divergence_count':unexplained,'policy_drift_detected':drift,'conscious_policy_evolution':conscious,'alerts':alerts,'topic_drift':topic_drift,'history':normalized,'human_policy_review_required':drift,'automatic_policy_change':False,'automatic_decision':False,'next_action':'Documenteer en bevestig expliciet of dit bewuste beleidsontwikkeling is.' if drift else 'Blijf besluitconsistentie periodiek volgen.'}
