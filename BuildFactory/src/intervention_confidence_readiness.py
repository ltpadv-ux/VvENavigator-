"""Enterprise 10.9 Intervention Confidence Score & Decision Readiness."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='10.9.0'
EVIDENCE_SCORE={'STERK':100.0,'REDELIJK':75.0,'BEPERKT':50.0}
WEIGHTS={'data_quality':25,'comparable_cases':20,'evidence_strength':20,'model_consistency':20,'scenario_uncertainty':15}

def _num(v:Any,default:float=0.0)->float:
    try:return float(v if v is not None else default)
    except (TypeError,ValueError):return default

def _clamp(v:float)->float:return max(0.0,min(100.0,v))

def score_intervention_confidence(recommendation_result:dict[str,Any], context:dict[str,Any]|None=None)->dict[str,Any]:
    context=context or {}; recs=recommendation_result.get('recommendations',[]) or []
    if recommendation_result.get('status')!='BEWIJSGESTUURDE AANBEVELING BESCHIKBAAR' or not recs:
        return {'intervention_confidence_readiness_version':ENGINE_VERSION,'status':'ONVOLDOENDE ADVIESDATA','recommendations':[],'decision_readiness':'NIET BESLUITRIJP','human_decision_required':True,'automatic_decision':False}
    dq=_clamp(_num(context.get('data_quality_score',85),85))
    model=_clamp(_num(context.get('model_consistency_score',80),80))
    uncertainty=_clamp(_num(context.get('scenario_uncertainty_score',25),25))
    out=[]
    for rec in recs:
        cases=_clamp(min(100.0,_num(rec.get('case_count'))/5.0*100.0))
        evidence=EVIDENCE_SCORE.get(str(rec.get('evidence_strength','BEPERKT')).upper(),50.0)
        similarity=_clamp(_num(rec.get('similarity_score')))
        consistency=_clamp((model*0.7)+(similarity*0.3))
        certainty=_clamp(100.0-uncertainty)
        components={'data_quality':dq,'comparable_cases':cases,'evidence_strength':evidence,'model_consistency':consistency,'scenario_uncertainty':certainty}
        confidence=round(sum(components[k]*WEIGHTS[k]/100 for k in WEIGHTS),1)
        level='HOOG' if confidence>=85 else ('REDELIJK' if confidence>=70 else ('MATIG' if confidence>=55 else 'LAAG'))
        readiness='BESLUITRIJP' if confidence>=80 and similarity>=70 and evidence>=75 else ('NADER ONDERZOEK' if confidence>=60 else 'NIET BESLUITRIJP')
        out.append({**rec,'confidence_score':confidence,'confidence_level':level,'decision_readiness':readiness,'confidence_components':components})
    out.sort(key=lambda x:(x['confidence_score'],x.get('ranking_score',0)),reverse=True)
    best=out[0]
    overall='BESLUITRIJP' if any(x['decision_readiness']=='BESLUITRIJP' for x in out) else ('NADER ONDERZOEK' if any(x['decision_readiness']=='NADER ONDERZOEK' for x in out) else 'NIET BESLUITRIJP')
    return {'intervention_confidence_readiness_version':ENGINE_VERSION,'status':'CONFIDENCE BEOORDEELD','decision_readiness':overall,'recommendation_count':len(out),'recommendations':out,'best_recommendation':best,'weights':WEIGHTS,'human_decision_required':True,'automatic_decision':False,'automatic_intervention':False,'automatic_policy_change':False,'next_action':'Leg besluitvoorstel voor aan Bestuur/ALV.' if overall=='BESLUITRIJP' else 'Versterk datakwaliteit, vergelijkbare cases of scenario-onderbouwing voordat besluitvorming plaatsvindt.'}
