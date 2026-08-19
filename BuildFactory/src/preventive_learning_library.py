"""Enterprise 10.7 Preventive Learning & Intervention Effectiveness Library."""
from __future__ import annotations
from hashlib import sha256
from statistics import mean
from typing import Any
ENGINE_VERSION='10.7.0'

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _id(*parts:Any)->str:
    return 'PLE-'+sha256('|'.join(str(x) for x in parts).encode()).hexdigest()[:10].upper()

def update_preventive_learning_library(effectiveness:dict[str,Any], mandate_result:dict[str,Any], context:dict[str,Any]|None=None, library:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; library=library or {}; entries=list(library.get('entries',[]) or [])
    mandate=mandate_result.get('mandate',{}) or {}; verification=effectiveness.get('verification',{}) or {}
    if not mandate or effectiveness.get('status') not in {'PREVENTIEF EFFECT BEWEZEN','DEELS EFFECTIEF','NADER HERSTEL NODIG'}:
        return {'preventive_learning_library_version':ENGINE_VERSION,'status':'GEEN LEERCASE BESCHIKBAAR','entries':entries,'recommendations':[],'automatic_policy_change':False}
    profile=str(context.get('vve_profile','standaard-vve')); risk_type=str(context.get('risk_type',context.get('domain','algemeen'))); intervention=str(mandate.get('scenario','VROEG INGRIJPEN'))
    entry_id=_id(mandate.get('mandate_id',''),risk_type,profile)
    entry={'learning_id':entry_id,'mandate_id':mandate.get('mandate_id',''),'profile':profile,'risk_type':risk_type,'intervention':intervention,'effectiveness_status':effectiveness.get('status'),'effectiveness_score':_num(effectiveness.get('effectiveness_score')),'actual_spend':_num(verification.get('actual_spend')),'verified_avoided_recovery_cost':_num(verification.get('verified_avoided_recovery_cost')),'health_uplift':_num(verification.get('health_uplift_vs_baseline')),'risk_reduction':_num(verification.get('risk_reduction_vs_baseline')),'evidence_count':len(mandate.get('evidence',[]) or [])}
    entry['value_per_euro']=round((entry['verified_avoided_recovery_cost']+max(0,entry['health_uplift'])*1000+max(0,entry['risk_reduction'])*750)/max(1,entry['actual_spend']),3)
    if not any(x.get('learning_id')==entry_id for x in entries): entries.append(entry)
    groups={}
    for e in entries:
        key=(e.get('profile'),e.get('risk_type'),e.get('intervention')); groups.setdefault(key,[]).append(e)
    recs=[]
    for (p,r,i),items in groups.items():
        recs.append({'profile':p,'risk_type':r,'intervention':i,'case_count':len(items),'avg_effectiveness_score':round(mean(_num(x.get('effectiveness_score')) for x in items),1),'avg_value_per_euro':round(mean(_num(x.get('value_per_euro')) for x in items),3),'avg_health_uplift':round(mean(_num(x.get('health_uplift')) for x in items),1),'avg_risk_reduction':round(mean(_num(x.get('risk_reduction')) for x in items),1),'evidence_strength':'STERK' if len(items)>=5 else ('REDELIJK' if len(items)>=3 else 'BEPERKT')})
    recs.sort(key=lambda x:(x['avg_effectiveness_score'],x['avg_value_per_euro'],x['case_count']),reverse=True)
    return {'preventive_learning_library_version':ENGINE_VERSION,'status':'LEERBIBLIOTHEEK BIJGEWERKT','entry_count':len(entries),'entries':entries,'recommendations':recs[:10],'best_known_intervention':recs[0] if recs else {},'human_validation_required':True,'automatic_policy_change':False,'automatic_intervention':False,'next_action':'Gebruik bewezen interventies als voorkeursoptie, maar laat Bestuur/ALV elke toepassing opnieuw beoordelen.'}
