"""Enterprise 10.8 Evidence-Based Intervention Recommendation Engine."""
from __future__ import annotations
from typing import Any
ENGINE_VERSION='10.8.0'
EVIDENCE_WEIGHT={'STERK':1.0,'REDELIJK':0.75,'BEPERKT':0.5}

def _num(v:Any)->float:
    try:return float(v or 0)
    except (TypeError,ValueError):return 0.0

def _similarity(case:dict[str,Any], context:dict[str,Any])->float:
    score=0.0
    if str(case.get('profile',''))==str(context.get('vve_profile','')): score+=0.45
    if str(case.get('risk_type',''))==str(context.get('risk_type',context.get('domain',''))): score+=0.45
    if str(case.get('intervention',''))==str(context.get('preferred_intervention','')) and context.get('preferred_intervention'): score+=0.10
    return min(1.0,score)

def recommend_evidence_based_interventions(trend_radar:dict[str,Any], learning_library:dict[str,Any], context:dict[str,Any]|None=None, top_n:int=5)->dict[str,Any]:
    context=context or {}
    alerts=trend_radar.get('early_intervention_alerts',[]) or []
    if not alerts:
        return {'evidence_based_intervention_recommendation_version':ENGINE_VERSION,'status':'GEEN ACTIEVE TRENDWAARSCHUWING','recommendations':[],'human_decision_required':True,'automatic_intervention':False}
    dominant=alerts[0]
    ctx={**context,'risk_type':context.get('risk_type',dominant.get('domain','algemeen'))}
    candidates=[]
    for rec in learning_library.get('recommendations',[]) or []:
        sim=_similarity(rec,ctx)
        effectiveness=_num(rec.get('avg_effectiveness_score'))/100
        evidence=EVIDENCE_WEIGHT.get(str(rec.get('evidence_strength','BEPERKT')).upper(),0.5)
        value=min(1.0,_num(rec.get('avg_value_per_euro'))/5.0)
        case_factor=min(1.0,_num(rec.get('case_count'))/5.0)
        ranking=round((sim*0.35+effectiveness*0.30+evidence*0.15+value*0.15+case_factor*0.05)*100,1)
        candidates.append({'profile':rec.get('profile'),'risk_type':rec.get('risk_type'),'intervention':rec.get('intervention'),'similarity_score':round(sim*100,1),'avg_effectiveness_score':_num(rec.get('avg_effectiveness_score')),'evidence_strength':rec.get('evidence_strength','BEPERKT'),'case_count':int(rec.get('case_count',0) or 0),'avg_value_per_euro':_num(rec.get('avg_value_per_euro')),'avg_health_uplift':_num(rec.get('avg_health_uplift')),'avg_risk_reduction':_num(rec.get('avg_risk_reduction')),'ranking_score':ranking})
    candidates.sort(key=lambda x:(x['ranking_score'],x['avg_effectiveness_score'],x['avg_value_per_euro']),reverse=True)
    ranked=candidates[:max(1,top_n)]
    return {'evidence_based_intervention_recommendation_version':ENGINE_VERSION,'status':'BEWIJSGESTUURDE AANBEVELING BESCHIKBAAR' if ranked else 'ONVOLDOENDE HISTORISCH BEWIJS','trigger':dominant,'context':ctx,'recommendation_count':len(ranked),'recommendations':ranked,'best_recommendation':ranked[0] if ranked else {},'ranking_weights':{'similarity':35,'effectiveness':30,'evidence_strength':15,'value_per_euro':15,'case_count':5},'human_decision_required':True,'automatic_intervention':False,'automatic_policy_change':False,'next_action':'Laat Bestuur/ALV de best passende bewezen interventies beoordelen in combinatie met actuele scenarioanalyse.' if ranked else 'Bouw eerst meer vergelijkbare, gevalideerde leercases op.'}
